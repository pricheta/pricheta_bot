from datetime import datetime

from pydantic import BaseModel


class MoneyTransfer(BaseModel):
    sender: str
    recipient: str
    amount: int
    created_at: datetime


class Debt(BaseModel):
    debtor: str
    creditor: str
    amount: int

    def __repr__(self) -> str:
        if not self.amount:
            return f'Между {self.debtor} и {self.creditor} нет задолженностей!'

        return f'{self.debtor} → {self.creditor}: {self.amount} ₽'
