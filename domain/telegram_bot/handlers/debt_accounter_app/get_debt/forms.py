from aiogram.fsm.state import StatesGroup, State


class DebtForm(StatesGroup):
    first_name = State()
    second_name = State()
