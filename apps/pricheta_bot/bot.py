import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_dialog import setup_dialogs

from apps.pricheta_bot.deps import (
    get_storage,
)
from domain.config import config
from domain.main_menu import main_router


async def main() -> None:
    dp = Dispatcher(storage=get_storage())
    dp.include_router(main_router)
    setup_dialogs(dp)

    bot = Bot(
        token=config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
