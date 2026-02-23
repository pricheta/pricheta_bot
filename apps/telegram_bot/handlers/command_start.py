from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)


START_MESSAGE = 'Привет! Я - бот для автоматизации рутины. Выбери приложение:'

DEBT_ACCOUNTER_BUTTON_TEXT = '📋 Долги'
DEBT_ACCOUNTER_BUTTON = InlineKeyboardButton(
    text=DEBT_ACCOUNTER_BUTTON_TEXT,
    callback_data=DEBT_ACCOUNTER_BUTTON_TEXT,
)

start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            DEBT_ACCOUNTER_BUTTON,
        ],
    ]
)


async def command_start_handler(message: Message) -> None:
    await message.answer(START_MESSAGE, reply_markup=start_keyboard)


async def open_debt_menu(callback: CallbackQuery) -> None:
    await callback.message.answer('Открываю учёт долгов...')  # type: ignore
    await callback.answer()
