from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

ROMA_NAME = 'Рома'
VLADA_NAME = 'Влада'
ROMA_AND_VLADA_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=ROMA_NAME),
            KeyboardButton(text=VLADA_NAME),
        ]
    ],
    resize_keyboard=True,
)


DEBT_ACCOUNTER_BUTTON_TEXT = '📋 Долги'
START_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=DEBT_ACCOUNTER_BUTTON_TEXT)],
    ],
    resize_keyboard=True,
)


TRANSFER_TEXT = '📋 Зафиксировать перевод'
GET_DEBT_TEXT = '📋 Узнать долг между двумя людьми'
DEBT_ACCOUNTER_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=TRANSFER_TEXT),
            KeyboardButton(text=GET_DEBT_TEXT),
        ],
    ],
    resize_keyboard=True,
)
