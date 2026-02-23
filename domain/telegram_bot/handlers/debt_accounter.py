from aiogram import Router, F
from aiogram.types import Message

from domain.config import config
from domain.models import MoneyTransfer
from domain.ports.asker import AskerPort
from domain.ports.debt_accounter import DebtAccounterPort


from domain.telegram_bot.handlers.keyboards import (
    DEBT_ACCOUNTER_KEYBOARD,
    DEBT_ACCOUNTER_BUTTON_TEXT,
    GET_DEBT_TEXT,
    ROMA_AND_VLADA_KEYBOARD,
    TRANSFER_TEXT,
    GET_TRANSFER_HISTORY_TEXT,
    REMOVE_KEYBOARD,
)

debt_accounter_router = Router()


@debt_accounter_router.message(F.text == DEBT_ACCOUNTER_BUTTON_TEXT)
async def open_debt_menu(message: Message) -> None:
    msg = 'Приложение "Долги". Выбери действие:'
    await message.answer(msg, reply_markup=DEBT_ACCOUNTER_KEYBOARD)


@debt_accounter_router.message(F.text == GET_DEBT_TEXT)
async def get_debt(
    message: Message, asker: AskerPort, debt_accounter: DebtAccounterPort
) -> None:
    ask_text = 'Введите первое имя:'
    first_person = await asker.ask(ask_text, message, [], ROMA_AND_VLADA_KEYBOARD)
    if not first_person:
        return

    ask_text = 'Введите второе имя (не может совпадать с первым):'
    second_person = await asker.ask(
        ask_text, message, [lambda x: x != first_person], ROMA_AND_VLADA_KEYBOARD
    )
    if not second_person:
        return

    debt = await debt_accounter.get_debt(first_person, second_person)
    await message.answer(str(debt), reply_markup=REMOVE_KEYBOARD)


@debt_accounter_router.message(F.text == TRANSFER_TEXT)
async def transfer(
    message: Message, asker: AskerPort, debt_accounter: DebtAccounterPort
) -> None:
    ask_text = 'Введите отправителя:'
    sender = await asker.ask(ask_text, message, [], ROMA_AND_VLADA_KEYBOARD)
    if not sender:
        return

    ask_text = 'Введите получателя (не может совпадать с отправителем):'
    recipient = await asker.ask(
        ask_text, message, [lambda x: x != sender], ROMA_AND_VLADA_KEYBOARD
    )
    if not recipient:
        return

    ask_text = 'Введите сумму перевода:'
    amount = await asker.ask(ask_text, message, [int, lambda x: int(x) > 0])
    if not amount:
        return

    transfer = MoneyTransfer(
        sender=sender,
        recipient=recipient,
        amount=int(amount),
    )

    old_debt = await debt_accounter.get_debt(transfer.sender, transfer.recipient)
    await debt_accounter.insert_transfer(transfer)
    debt = await debt_accounter.get_debt(transfer.sender, transfer.recipient)

    msg = (
        f'Перевод зафиксирован\n'
        f'{transfer}\n\n'
        f'Изначальный долг:\n'
        f'{old_debt}\n\n'
        f'Актуальный долг:\n'
        f'{debt}\n\n'
        f'Зафиксировал перевод: @{message.from_user.username}'
    )
    # await message.bot.send_message(-4732298768, msg)
    await message.answer(msg, reply_markup=REMOVE_KEYBOARD)


@debt_accounter_router.message(F.text == GET_TRANSFER_HISTORY_TEXT)
async def get_transfer_history(
    message: Message, asker: AskerPort, debt_accounter: DebtAccounterPort
) -> None:
    ask_text = 'Введите первое имя:'
    first_person = await asker.ask(ask_text, message, [], ROMA_AND_VLADA_KEYBOARD)
    if not first_person:
        return

    ask_text = 'Введите второе имя (не может совпадать с первым):'
    second_person = await asker.ask(
        ask_text, message, [lambda x: x != first_person], ROMA_AND_VLADA_KEYBOARD
    )
    if not second_person:
        return

    ask_text = f'Введите глубину истории в днях (по умолчанию {config.GET_TRANSFER_HISTORY_DEFAULT_LOOKBACK}):'
    lookback_days = await asker.ask(
        ask_text,
        message,
        [int, lambda x: int(x) > 0],
        default=str(config.GET_TRANSFER_HISTORY_DEFAULT_LOOKBACK),
    )
    if not lookback_days:
        return

    history = await debt_accounter.get_transfer_history(
        first_person, second_person, int(lookback_days)
    )

    msg = MoneyTransfer.history_str(history)
    await message.answer(msg, reply_markup=REMOVE_KEYBOARD)
