from functools import lru_cache

from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage

from adapters.debt_accounter.debt_accounter_client.client import (
    DebtAccounterClient,
)
from domain.ports.debt_accounter import DebtAccounterPort


@lru_cache(maxsize=1)
def get_storage() -> BaseStorage:
    return MemoryStorage()


@lru_cache(maxsize=1)
def get_debt_accounter() -> DebtAccounterPort:
    return DebtAccounterClient()
