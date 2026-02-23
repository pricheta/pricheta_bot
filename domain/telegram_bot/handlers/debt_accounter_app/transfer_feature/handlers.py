from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from domain.models import MoneyTransfer
from domain.ports.debt_accounter import DebtAccounterPort
from domain.telegram_bot.handlers.debt_accounter_app.transfer_feature.forms import (
    TransferForm,
)

TRANSFER_TEXT = '📋 Зафиксировать перевод'

transfer_router = Router()


@transfer_router.message(Command('transfer'))
@transfer_router.message(F.text == TRANSFER_TEXT)
async def transfer(message: Message, state: FSMContext) -> None:
    msg = 'Введите отправителя'
    await message.answer(msg)
    await state.set_state(TransferForm.sender)


@transfer_router.message(TransferForm.sender)
async def process_sender(message: Message, state: FSMContext) -> None:
    await state.update_data(sender=message.text)

    msg = 'Введите получателя:'
    await message.answer(msg)
    await state.set_state(TransferForm.recipient)


@transfer_router.message(TransferForm.recipient)
async def process_recipient(
    message: Message, state: FSMContext, debt_accounter: DebtAccounterPort
) -> None:
    await state.update_data(recipient=message.text)

    msg = 'Введите сумму перевода:'
    await message.answer(msg)
    await state.set_state(TransferForm.amount)


@transfer_router.message(TransferForm.amount)
async def process_amount(
    message: Message, state: FSMContext, debt_accounter: DebtAccounterPort
) -> None:
    try:
        amount = int(message.text)  # type: ignore
    except ValueError:
        await message.answer('Введите корректную сумму (целое положительное число):')
        return

    if amount < 0:
        await message.answer('Введите корректную сумму (целое положительное число):')
        return

    data = await state.get_data()
    await state.clear()

    sender = data['sender']
    recipient = data['recipient']

    transfer = MoneyTransfer(
        sender=sender,
        recipient=recipient,
        amount=amount,
    )
    await debt_accounter.insert_transfer(transfer)

    await message.answer(f'Перевод зафиксирован\n{transfer}')
