from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from domain.telegram_bot.handlers.debt_accounter_app.get_debt_feature.forms import (
    DebtForm,
)

GET_DEBT_TEXT = '📋 Узнать долг'

get_debt_router = Router()


@get_debt_router.message(F.text == GET_DEBT_TEXT)
async def get_debt(message: Message, state: FSMContext) -> None:
    msg = 'Введите первое имя'
    await message.answer(msg)
    await state.set_state(DebtForm.first_name)


@get_debt_router.message(DebtForm.first_name)
async def process_first_name(message: Message, state: FSMContext) -> None:
    await state.update_data(first_name=message.text)
    msg = 'Введите второе имя'
    await message.answer(msg)
    await state.set_state(DebtForm.second_name)


@get_debt_router.message(DebtForm.second_name)
async def process_second_name(message: Message, state: FSMContext) -> None:
    await state.update_data(second_name=message.text)
    data = await state.get_data()
    await state.clear()

    first = data['first_name']
    second = data['second_name']

    await message.answer(f'Ищу долг между пользователями {first} и {second}...')
