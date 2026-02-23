from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from domain.models import MoneyTransfer
from domain.ports.debt_accounter import DebtAccounterPort
from domain.telegram_bot.handlers.debt_accounter_app.transfer.forms import (
    TransferForm,
)
from domain.telegram_bot.handlers.keyboards import (
    TRANSFER_TEXT,
    ROMA_AND_VLADA_KEYBOARD,
)

transfer_router = Router()


@transfer_router.message(F.text == TRANSFER_TEXT)
async def transfer(message: Message, state: FSMContext) -> None:
    msg = 'Введите отправителя:'
    await message.answer(msg, reply_markup=ROMA_AND_VLADA_KEYBOARD)
    await state.set_state(TransferForm.sender)


@transfer_router.message(TransferForm.sender)
async def process_sender(message: Message, state: FSMContext) -> None:
    await state.update_data(sender=message.text)

    msg = 'Введите получателя:'
    await message.answer(msg, reply_markup=ROMA_AND_VLADA_KEYBOARD)
    await state.set_state(TransferForm.recipient)


@transfer_router.message(TransferForm.recipient)
async def process_recipient(
    message: Message,
    state: FSMContext,
) -> None:
    data = await state.get_data()
    sender = data['sender']
    recipient = message.text

    if sender == recipient:
        msg = 'Отправитель и получатель не должны совпадать, повторите попытку:'
        await message.answer(msg, reply_markup=ROMA_AND_VLADA_KEYBOARD)
        return

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

    await state.update_data(amount=message.text)
    data = await state.get_data()
    await state.clear()

    transfer = MoneyTransfer.model_validate(data)
    old_debt = await debt_accounter.get_debt(transfer.sender, transfer.recipient)
    await debt_accounter.insert_transfer(transfer)
    debt = await debt_accounter.get_debt(transfer.sender, transfer.recipient)

    msg = (
        f'Перевод зафиксирован\n'
        f'{transfer}\n\n'
        f'Изначальный долг:\n'
        f'{old_debt}\n\n'
        f'Актуальный долг:\n'
        f'{debt}\n\n'
        f'Зафиксировал перевод: @{message.from_user.username}'  # type: ignore
    )
    # await message.bot.send_message(-4732298768, msg)  # type: ignore
    await message.answer(msg)
