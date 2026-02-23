from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
)

from domain.telegram_bot.handlers.keyboards import START_KEYBOARD

command_start_router = Router()


@command_start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer('Бот не работает, он в разработке')
    # msg = 'Привет! Я - бот для автоматизации рутины от @pricheta. Выбери приложение:'
    # await message.answer(msg, reply_markup=START_KEYBOARD)
