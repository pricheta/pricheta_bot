from typing import Iterable, Callable, Any

from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram_input import InputManager

from domain.ports.asker import AskerPort, validator
from domain.telegram_bot.handlers.keyboards import (
    BY_DEFAULT_KEYBOARD,
    REMOVE_KEYBOARD,
    BY_DEFAULT,
)


class AiogramInputAsker(AskerPort):
    def __init__(self, dispatcher: Dispatcher) -> None:
        self.asker = InputManager(dispatcher)

    async def ask(
        self,
        ask_text: str,
        message: Message,
        validators: Iterable[validator],
        reply_markup: ReplyKeyboardMarkup | ReplyKeyboardRemove = REMOVE_KEYBOARD,
        default: str | None = None,
    ) -> str | None:
        if default is not None:
            reply_markup = BY_DEFAULT_KEYBOARD

        while True:
            await message.answer(ask_text, reply_markup=reply_markup)
            value = await self.asker.input(message.chat.id, timeout=30)

            if not value:
                return None

            value_text = value.text
            if value_text == BY_DEFAULT and default is not None:
                value_text = default

            validated = self.run_validators(value_text, validators)

            if validated:
                return value_text
