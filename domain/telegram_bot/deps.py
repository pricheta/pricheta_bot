from functools import lru_cache

from aiohttp import ClientSession

from adapters.debt_accounter.debt_accounter_client.client import (
    DebtAccounterAsyncClient,
)
from domain.ports.debt_accounter import DebtAccounterPort


@lru_cache(maxsize=1)
def get_debt_accounter() -> DebtAccounterPort:
    debt_accounter_session = ClientSession()
    return DebtAccounterAsyncClient(debt_accounter_session)
