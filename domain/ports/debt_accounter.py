from typing import Protocol

from domain.models import MoneyTransfer, Debt


class DebtAccounterPort(Protocol):
    def insert_transfer(self, transfer: MoneyTransfer) -> None: ...

    def get_transfer_history(
        self, first_person: str, second_person: str, lookback_days: int
    ) -> list[MoneyTransfer]: ...

    def get_debt(self, first_person: str, second_person: str) -> Debt: ...
