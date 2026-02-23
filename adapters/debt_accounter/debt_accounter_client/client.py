from aiohttp import ClientSession

from adapters.debt_accounter.debt_accounter_client.config import \
    DebtAccounterClientConfig
from domain.models import Debt, MoneyTransfer
from domain.ports.debt_accounter import DebtAccounterPort


class DebtAccounterAsyncClient(DebtAccounterPort):
    def __init__(self, session: ClientSession):
        self. config = DebtAccounterClientConfig() # type: ignore
        self._session = session

    async def get_debt(self, first_person: str, second_person: str) -> Debt:
        url = f"{self.config.HOST}/debt/"
        params = {
            "first_person": first_person,
            "second_person": second_person,
        }

        async with self._session.get(url, params=params) as response:
            response.raise_for_status()
            return Debt.model_validate(await response.json())

    async def get_transfer_history(
        self, first_person: str, second_person: str, lookback_days: int
    ) -> list[MoneyTransfer]:
        raise NotImplementedError()

    async def insert_transfer(self, transfer: MoneyTransfer) -> None:
        raise NotImplementedError()