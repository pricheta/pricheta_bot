from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


DEBT_ACCOUNTER_BUTTON_TEXT = '📋 Долги'

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=DEBT_ACCOUNTER_BUTTON_TEXT)],
    ],
    resize_keyboard=True,
)


async def command_start_handler(message: Message) -> None:
    msg = 'Привет! Я - бот для автоматизации рутины от @pricheta. Выбери приложение:'
    await message.answer(msg, reply_markup=start_keyboard)
