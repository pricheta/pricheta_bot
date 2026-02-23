from aiogram.fsm.state import StatesGroup, State


class TransferForm(StatesGroup):
    sender = State()
    recipient = State()
    amount = State()
