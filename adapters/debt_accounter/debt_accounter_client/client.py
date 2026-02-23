from aiohttp import ClientSession

from adapters.debt_accounter.debt_accounter_client.config import (
    DebtAccounterClientConfig,
)
from domain.models import Debt, MoneyTransfer
from domain.ports.debt_accounter import DebtAccounterPort


class DebtAccounterAsyncClient(DebtAccounterPort):
    def __init__(self, session: ClientSession) -> None:
        self.config = DebtAccounterClientConfig()  # type: ignore
        self._session = session

    async def get_debt(self, first_person: str, second_person: str) -> Debt:
        url = f'{self.config.HOST}/debt/'
        params = {
            'first_person': first_person,
            'second_person': second_person,
        }

        async with self._session.get(url, params=params) as response:
            response.raise_for_status()
            return Debt.model_validate(await response.json())

    async def get_transfer_history(
        self, first_person: str, second_person: str, lookback_days: int
    ) -> list[MoneyTransfer]:
        url = f'{self.config.HOST}/transfer_history/'
        params = {
            'first_person': first_person,
            'second_person': second_person,
            'lookback_days': lookback_days,
        }

        async with self._session.get(url, params=params) as response:  # type: ignore
            response.raise_for_status()
            data = await response.json()

        return [MoneyTransfer.model_validate(obj) for obj in data]

    async def insert_transfer(self, transfer: MoneyTransfer) -> None:
        url = f'{self.config.HOST}/transfer/'

        async with self._session.post(url, json=transfer.model_dump()) as response:
            response.raise_for_status()
