from aiogram.types import (
    Message,
    MenuButtonCommands,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

START_MESSAGE = 'Привет! Я - бот для автоматизации рутины. Выбери приложение'

DEBT_ACCOUNTER_BUTTON_TEXT = '📋 Долги'

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=DEBT_ACCOUNTER_BUTTON_TEXT)],
    ],
    resize_keyboard=True,
)


async def command_start_handler(message: Message) -> None:
    await message.answer(START_MESSAGE, reply_markup=start_keyboard)
