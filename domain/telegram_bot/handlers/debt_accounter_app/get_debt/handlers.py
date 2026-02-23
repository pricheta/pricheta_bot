from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from domain.ports.debt_accounter import DebtAccounterPort
from domain.telegram_bot.handlers.debt_accounter_app.get_debt.forms import (
    DebtForm,
)
from domain.telegram_bot.handlers.keyboards import (
    GET_DEBT_TEXT,
    ROMA_AND_VLADA_KEYBOARD,
)

get_debt_router = Router()


@get_debt_router.message(F.text == GET_DEBT_TEXT)
async def get_debt(message: Message, state: FSMContext) -> None:
    msg = 'Введите первое имя:'
    await message.answer(msg, reply_markup=ROMA_AND_VLADA_KEYBOARD)
    await state.set_state(DebtForm.first_name)


@get_debt_router.message(DebtForm.first_name)
async def process_first_name(message: Message, state: FSMContext) -> None:
    await state.update_data(first_name=message.text)
    msg = 'Введите второе имя:'
    await message.answer(msg, reply_markup=ROMA_AND_VLADA_KEYBOARD)
    await state.set_state(DebtForm.second_name)


@get_debt_router.message(DebtForm.second_name)
async def process_second_name(
    message: Message, state: FSMContext, debt_accounter: DebtAccounterPort
) -> None:
    data = await state.get_data()
    first_person = data['first_name']
    second_person = message.text

    if first_person == second_person:
        msg = 'Имена не должны повторяться, повторите попытку:'
        await message.answer(msg)
        return

    await state.clear()

    debt = await debt_accounter.get_debt(first_person, second_person)  # type: ignore
    await message.answer(str(debt))
