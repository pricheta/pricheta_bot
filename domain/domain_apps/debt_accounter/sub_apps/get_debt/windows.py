from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const, Format

from apps.pricheta_bot.deps import get_debt_accounter
from domain.const import ROMA_NAME, VLADA_NAME

debt_accounter = get_debt_accounter()


async def get_result(**_) -> dict[str, str]:
    debt = debt_accounter.get_debt(ROMA_NAME, VLADA_NAME)
    return {'msg': str(debt)}


class GetDebtStatesGroup(StatesGroup):
    show_result = State()


get_debt_dialog = Dialog(
    Window(
        Format('{msg}'),
        Cancel(Const('Назад')),
        state=GetDebtStatesGroup.show_result,
        getter=get_result,
    ),
)
