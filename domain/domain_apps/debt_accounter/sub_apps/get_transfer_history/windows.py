from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Cancel, Select
from aiogram_dialog.widgets.text import Const, Format

from apps.pricheta_bot.deps import get_debt_accounter
from domain.const import ROMA_NAME, VLADA_NAME
from domain.models import MoneyTransfer

debt_accounter = get_debt_accounter()


class GetTransferHistoryStatesGroup(StatesGroup):
    enter_lookup_days = State()
    show_result = State()


async def lookup_days_entered(
    _: CallbackQuery, __: Select, manager: DialogManager, lookup_days: str
) -> None:
    manager.dialog_data.update(lookup_days=lookup_days)
    await manager.switch_to(GetTransferHistoryStatesGroup.show_result)


async def get_final_message(dialog_manager: DialogManager, **_) -> dict[str, str]:
    lookup_days = dialog_manager.dialog_data.get('lookup_days')
    history = debt_accounter.get_transfer_history(ROMA_NAME, VLADA_NAME, lookup_days)

    return {'msg': MoneyTransfer.history_str(history)}


get_transfer_history_dialog = Dialog(
    Window(
        Format('За сколько дней отобразить историю?'),
        Select(
            text=Format('{item}'),
            id='enter_lookup_days',
            item_id_getter=lambda item: item,
            items=[7, 14, 21, 28],
            on_click=lookup_days_entered,
        ),
        Cancel(Const('Назад')),
        state=GetTransferHistoryStatesGroup.enter_lookup_days,
    ),
    Window(
        Format('{msg}'),
        Cancel(Const('Закончить')),
        state=GetTransferHistoryStatesGroup.show_result,
        getter=get_final_message,
    ),
)
