from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

GET_DEBT_TEXT = '📋 Узнать долг'

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=GET_DEBT_TEXT)],
    ],
    resize_keyboard=True,
)


async def open_debt_menu(message: Message) -> None:
    msg = 'Приложение "Долги". Выбери действие:'
    await message.answer(msg, reply_markup=start_keyboard)


async def get_debt(message: Message) -> None:
    await message.answer('Приложение "Долги"')
