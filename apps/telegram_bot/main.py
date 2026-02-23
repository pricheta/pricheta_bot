import asyncio
import logging
import sys
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

from apps.telegram_bot.config import BotConfig
from apps.telegram_bot.handlers.command_start import (
    command_start_handler,
    DEBT_ACCOUNTER_BUTTON_TEXT,
    open_debt_menu,
)

load_dotenv()
config = BotConfig()  # type: ignore


dp = Dispatcher()
dp.message(CommandStart())(command_start_handler)

dp.callback_query(F.data == DEBT_ACCOUNTER_BUTTON_TEXT)(open_debt_menu)


async def main() -> None:
    bot = Bot(
        token=config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
