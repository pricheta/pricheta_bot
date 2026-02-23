from datetime import datetime

from pydantic import BaseModel


class MoneyTransfer(BaseModel):
    sender: str
    recipient: str
    amount: int
    created_at: datetime | None = None

    def __str__(self) -> str:
        return (
            f'Отправитель {self.sender} | Получатель {self.recipient} | {self.amount} ₽'
        )

    def __repr__(self) -> str:
        return self.__str__()


class Debt(BaseModel):
    debtor: str
    creditor: str
    amount: int

    def __str__(self) -> str:
        if not self.amount:
            return f'{self.debtor} | {self.creditor} | {self.amount} ₽'

        return f'Заемщик {self.debtor} | Должник {self.creditor} | {self.amount} ₽'

    def __repr__(self) -> str:
        return self.__str__()
