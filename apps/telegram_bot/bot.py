import asyncio
import logging
import sys


from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from domain.config import config
from apps.telegram_bot.deps import (
    get_debt_accounter,
    get_debt_accounter_session,
    get_asker,
)
from domain.telegram_bot.handlers.command_start import command_start_router
from domain.telegram_bot.handlers.debt_accounter import debt_accounter_router


async def main() -> None:
    dp = Dispatcher()
    dp.include_routers(command_start_router, debt_accounter_router)

    dp['asker'] = get_asker(dp)
    dp['debt_accounter'] = get_debt_accounter()

    debt_accounter_session = get_debt_accounter_session()

    bot = Bot(
        token=config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    try:
        await dp.start_polling(bot)
    except Exception:
        await debt_accounter_session.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
