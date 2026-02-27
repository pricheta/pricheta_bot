from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from domain.domain_apps.debt_accounter.menu import (
    DebtAccounterStatesGroup,
    debt_accounter_dialog,
)
from domain.domain_apps.debt_accounter.sub_apps.get_debt.windows import get_debt_dialog
from domain.domain_apps.debt_accounter.sub_apps.get_transfer_history.windows import (
    get_transfer_history_dialog,
)
from domain.domain_apps.debt_accounter.sub_apps.insert_transfer.windows import (
    insert_transfer_dialog,
)


class MainMenuStatesGroup(StatesGroup):
    main_menu = State()


main_menu_dialog = Dialog(
    Window(
        Const(
            'Привет! Я - бот для автоматизации рутины от @pricheta. Выберите приложение'
        ),
        Start(
            Const('Приложение Долги'),
            id='debt_accounter_button',
            state=DebtAccounterStatesGroup.menu,
        ),
        state=MainMenuStatesGroup.main_menu,
    ),
)


main_router = Router()
main_router.include_routers(
    main_menu_dialog,
    debt_accounter_dialog,
    get_debt_dialog,
    insert_transfer_dialog,
    get_transfer_history_dialog,
)


@main_router.message(CommandStart())
async def start_command(_: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(
        MainMenuStatesGroup.main_menu, mode=StartMode.RESET_STACK
    )
