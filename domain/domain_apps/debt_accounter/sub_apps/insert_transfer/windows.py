from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Back, Cancel, Select
from aiogram_dialog.widgets.text import Const, Format

from apps.pricheta_bot.deps import get_debt_accounter
from domain.config import config
from domain.const import ROMA_NAME, VLADA_NAME
from domain.models import MoneyTransfer

debt_accounter = get_debt_accounter()


class InsertTransferStatesGroup(StatesGroup):
    enter_sender = State()
    enter_amount = State()
    show_result = State()


async def sender_chosen(
    _: CallbackQuery, __: Select, manager: DialogManager, sender: str
) -> None:
    manager.dialog_data.update(sender=sender)
    await manager.switch_to(InsertTransferStatesGroup.enter_amount)


async def amount_entered(
    _: CallbackQuery, __: Select, manager: DialogManager, amount: str
) -> None:
    old_debt = debt_accounter.get_debt(ROMA_NAME, VLADA_NAME)
    manager.dialog_data.update(old_debt=old_debt)

    sender = manager.dialog_data.get('sender')
    recipient = ROMA_NAME if sender == VLADA_NAME else VLADA_NAME

    transfer = MoneyTransfer(sender=sender, recipient=recipient, amount=int(amount))
    debt_accounter.insert_transfer(transfer)

    new_debt = debt_accounter.get_debt(ROMA_NAME, VLADA_NAME)
    manager.dialog_data.update(new_debt=new_debt)

    manager.dialog_data.update(transfer=transfer)
    await manager.switch_to(InsertTransferStatesGroup.show_result)


async def get_result(dialog_manager: DialogManager, **_) -> dict[str, str]:
    old_debt = dialog_manager.dialog_data.get('old_debt')
    new_debt = dialog_manager.dialog_data.get('new_debt')
    transfer = dialog_manager.dialog_data.get('transfer')

    msg = (
        f'Перевод зафиксирован\n'
        f'{transfer}\n\n'
        f'Изначальный долг:\n'
        f'{old_debt}\n\n'
        f'Актуальный долг:\n'
        f'{new_debt}\n\n'
    )

    bot = dialog_manager.middleware_data.get('bot')
    if config.COMMON_CHANNEL:
        await bot.send_message(-4732298768, msg)

    return {'msg': msg}


insert_transfer_dialog = Dialog(
    Window(
        Format('Выберите отправителя'),
        Select(
            text=Format('{item}'),
            id='enter_sender',
            item_id_getter=lambda item: item,
            items=[ROMA_NAME, VLADA_NAME],
            on_click=sender_chosen,
        ),
        Cancel(Const('Назад')),
        state=InsertTransferStatesGroup.enter_sender,
    ),
    Window(
        Format('Введите сумму'),
        TextInput(
            id='enter_amount',
            filter=lambda x: int(x.text) > 0,
            on_success=amount_entered,
        ),
        Back(Const('Назад')),
        state=InsertTransferStatesGroup.enter_amount,
    ),
    Window(
        Format('{msg}'),
        Cancel(Const('Закончить')),
        state=InsertTransferStatesGroup.show_result,
        getter=get_result,
    ),
)
