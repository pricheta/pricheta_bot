from aiogram.fsm.state import StatesGroup, State


class TransferHistory(StatesGroup):
    first_name = State()
    second_name = State()
    lookback_days = State()
