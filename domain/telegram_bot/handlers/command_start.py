from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from domain.telegram_bot.handlers.debt_accounter_app.app import (
    DEBT_ACCOUNTER_BUTTON_TEXT,
)

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=DEBT_ACCOUNTER_BUTTON_TEXT)],
    ],
    resize_keyboard=True,
)

command_start_router = Router()


@command_start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    msg = 'Привет! Я - бот для автоматизации рутины от @pricheta. Выбери приложение:'
    await message.answer(msg, reply_markup=start_keyboard)
