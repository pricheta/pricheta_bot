from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel


class MoneyTransfer(BaseModel):
    sender: str
    recipient: str
    amount: int
    created_at: datetime | None = None

    def __str__(self) -> str:
        str_ = ''

        if self.created_at:
            str_ += f'{self.created_at.astimezone(ZoneInfo("Europe/Moscow")).strftime(format="%d.%m %H:%M")} | '

        str_ += (
            f'Отправитель {self.sender} | Получатель {self.recipient} | {self.amount} ₽'
        )

        return str_

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def history_str(transfers: list['MoneyTransfer']) -> str:
        str_transfers = map(str, transfers)
        return '\n'.join(str_transfers)


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
