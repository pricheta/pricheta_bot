from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from domain.models import MoneyTransfer
from domain.ports.debt_accounter import DebtAccounterPort
from domain.telegram_bot.handlers.debt_accounter_app.get_transfer_history.forms import (
    TransferHistory,
)
from domain.telegram_bot.handlers.keyboards import (
    ROMA_AND_VLADA_KEYBOARD,
    GET_TRANSFER_HISTORY_TEXT,
    BY_DEFAULT_KEYBOARD,
    BY_DEFAULT,
)

get_transfer_history_router = Router()


@get_transfer_history_router.message(F.text == GET_TRANSFER_HISTORY_TEXT)
async def get_transfer_history(message: Message, state: FSMContext) -> None:
    msg = 'Введите первое имя:'
    await message.answer(msg, reply_markup=ROMA_AND_VLADA_KEYBOARD)
    await state.set_state(TransferHistory.first_name)


@get_transfer_history_router.message(TransferHistory.first_name)
async def process_first_name(message: Message, state: FSMContext) -> None:
    await state.update_data(first_name=message.text)

    msg = 'Введите второе имя:'
    await message.answer(msg, reply_markup=ROMA_AND_VLADA_KEYBOARD)
    await state.set_state(TransferHistory.second_name)


@get_transfer_history_router.message(TransferHistory.second_name)
async def process_second_name(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    first_person = data['first_name']
    second_person = message.text

    if first_person == second_person:
        msg = 'Имена не должны повторяться, повторите попытку:'
        await message.answer(msg)
        return

    await state.update_data(second_name=message.text)

    msg = 'Введите глубину истории в днях (по умолчанию 7):'
    await message.answer(msg, reply_markup=BY_DEFAULT_KEYBOARD)
    await state.set_state(TransferHistory.lookback_days)


@get_transfer_history_router.message(TransferHistory.lookback_days)
async def process_lookback_days(
    message: Message, state: FSMContext, debt_accounter: DebtAccounterPort
) -> None:
    text = message.text

    if text == BY_DEFAULT:
        text = '7'

    try:
        amount = int(text)  # type: ignore
    except ValueError:
        await message.answer('Введите корректную сумму (целое положительное число):')
        return

    if amount < 0:
        await message.answer('Введите корректную сумму (целое положительное число):')
        return

    await state.update_data(lookback_days=text)
    data = await state.get_data()
    await state.clear()

    first_name = data['first_name']
    second_name = data['second_name']
    lookback_days = data['lookback_days']

    history = await debt_accounter.get_transfer_history(
        first_name, second_name, lookback_days
    )

    msg = MoneyTransfer.history_str(history)
    await message.answer(msg, reply_markup=ReplyKeyboardRemove())
