import requests

from adapters.debt_accounter.debt_accounter_client.config import (
    DebtAccounterClientConfig,
)
from domain.models import Debt, MoneyTransfer
from domain.ports.debt_accounter import DebtAccounterPort


class DebtAccounterClient(DebtAccounterPort):
    def __init__(self) -> None:
        self.config = DebtAccounterClientConfig()

    def get_debt(self, first_person: str, second_person: str) -> Debt:
        url = f'{self.config.HOST}/debt/'
        params = {
            'first_person': first_person,
            'second_person': second_person,
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        return Debt.model_validate(response.json())

    def get_transfer_history(
        self, first_person: str, second_person: str, lookback_days: int
    ) -> list[MoneyTransfer]:
        url = f'{self.config.HOST}/transfer_history/'
        params = {
            'first_person': first_person,
            'second_person': second_person,
            'lookback_days': lookback_days,
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return [MoneyTransfer.model_validate(obj) for obj in data]

    def insert_transfer(self, transfer: MoneyTransfer) -> None:
        url = f'{self.config.HOST}/transfer/'

        response = requests.post(url, json=transfer.model_dump())
        response.raise_for_status()
