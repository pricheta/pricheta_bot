import asyncio
import logging
import sys

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from domain.telegram_bot.config import BotConfig
from domain.telegram_bot.deps import get_debt_accounter
from domain.telegram_bot.handlers.command_start import command_start_router
from domain.telegram_bot.handlers.debt_accounter_app.app import debt_accounter_router

load_dotenv()


async def main() -> None:
    dp = Dispatcher()
    dp.include_routers(command_start_router, debt_accounter_router)
    dp['debt_accounter'] = get_debt_accounter()

    config = BotConfig()  # type: ignore
    bot = Bot(
        token=config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
