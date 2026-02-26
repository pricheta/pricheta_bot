from functools import lru_cache

from aiogram import Dispatcher
from aiohttp import ClientSession

from adapters.asker.aiogram_input.asker import AiogramInputAsker
from adapters.debt_accounter.debt_accounter_client.client import (
    DebtAccounterAsyncClient,
)
from domain.ports.asker import AskerPort
from domain.ports.debt_accounter import DebtAccounterPort


@lru_cache(maxsize=1)
def get_debt_accounter_session() -> ClientSession:
    return ClientSession()


@lru_cache(maxsize=1)
def get_debt_accounter() -> DebtAccounterPort:
    debt_accounter_session = get_debt_accounter_session()
    return DebtAccounterAsyncClient(debt_accounter_session)


@lru_cache(maxsize=1)
def get_asker(dp: Dispatcher) -> AskerPort:
    return AiogramInputAsker(dp)
