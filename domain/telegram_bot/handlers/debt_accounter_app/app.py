from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from domain.telegram_bot.handlers.debt_accounter_app.get_debt_feature.handlers import (
    GET_DEBT_TEXT,
    get_debt_router,
    GET_DEBT_VLADA_AND_ROMA_TEXT,
)

DEBT_ACCOUNTER_BUTTON_TEXT = '📋 Долги'

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=GET_DEBT_TEXT)],
        [KeyboardButton(text=GET_DEBT_VLADA_AND_ROMA_TEXT)],
    ],
    resize_keyboard=True,
)


debt_accounter_router = Router()
debt_accounter_router.include_router(get_debt_router)


@debt_accounter_router.message(Command('debt'))
@debt_accounter_router.message(F.text == DEBT_ACCOUNTER_BUTTON_TEXT)
async def open_debt_menu(message: Message) -> None:
    msg = 'Приложение "Долги". Выбери действие:'
    await message.answer(msg, reply_markup=start_keyboard)
