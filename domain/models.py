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
