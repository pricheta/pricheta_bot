from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from domain.telegram_bot.handlers.debt_accounter_app.get_debt.handlers import (
    get_debt_router,
)
from domain.telegram_bot.handlers.debt_accounter_app.transfer.handlers import (
    transfer_router,
)
from domain.telegram_bot.handlers.keyboards import (
    DEBT_ACCOUNTER_KEYBOARD,
    DEBT_ACCOUNTER_BUTTON_TEXT,
)

debt_accounter_router = Router()
debt_accounter_router.include_routers(get_debt_router, transfer_router)


@debt_accounter_router.message(Command('debt'))
@debt_accounter_router.message(F.text == DEBT_ACCOUNTER_BUTTON_TEXT)
async def open_debt_menu(message: Message) -> None:
    msg = 'Приложение "Долги". Выбери действие:'
    await message.answer(msg, reply_markup=DEBT_ACCOUNTER_KEYBOARD)
