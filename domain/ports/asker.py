from typing import Protocol, Callable, Any, Iterable

from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

from domain.telegram_bot.handlers.keyboards import REMOVE_KEYBOARD

validator = Callable[[Any], bool]


class AskerPort(Protocol):
    async def ask(
        self,
        ask_text: str,
        message: Message,
        validators: Iterable[validator],
        reply_markup: ReplyKeyboardMarkup | ReplyKeyboardRemove = REMOVE_KEYBOARD,
        default: str | None = None,
    ) -> str | None: ...

    @staticmethod
    def run_validators(str_: str, validators: Iterable[validator]) -> bool:
        for validator in validators:
            try:
                result = validator(str_)
            except:
                return False

            if not result:
                return False

        return True
