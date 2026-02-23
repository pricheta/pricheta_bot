from typing import Protocol

from domain.models import MoneyTransfer, Debt


class DebtAccounterPort(Protocol):
    async def insert_transfer(self, transfer: MoneyTransfer) -> None: ...

    async def get_transfer_history(
        self, first_person: str, second_person: str, lookback_days: int
    ) -> list[MoneyTransfer]: ...

    async def get_debt(self, first_person: str, second_person: str) -> Debt: ...
