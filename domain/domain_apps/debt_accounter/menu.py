from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel, Start
from aiogram_dialog.widgets.text import Const

from domain.domain_apps.debt_accounter.sub_apps.get_debt.windows import (
    GetDebtStatesGroup,
)
from domain.domain_apps.debt_accounter.sub_apps.get_transfer_history.windows import (
    GetTransferHistoryStatesGroup,
)
from domain.domain_apps.debt_accounter.sub_apps.insert_transfer.windows import (
    InsertTransferStatesGroup,
)


class DebtAccounterStatesGroup(StatesGroup):
    menu = State()


debt_accounter_dialog = Dialog(
    Window(
        Const('Приложение Долги. Выберите действие'),
        Start(
            Const('Узнать долг'),
            id='get_debt_button',
            state=GetDebtStatesGroup.show_result,
        ),
        Start(
            Const('Зафиксировать перевод'),
            id='insert_transfer_button',
            state=InsertTransferStatesGroup.enter_sender,
        ),
        Start(
            Const('Получить историю переводов'),
            id='get_transfer_history_button',
            state=GetTransferHistoryStatesGroup.enter_lookup_days,
        ),
        Cancel(Const('Назад')),
        state=DebtAccounterStatesGroup.menu,
    ),
)
