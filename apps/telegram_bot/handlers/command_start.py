from aiogram.types import Message

START_MESSAGE = "Hello, my name is Roma!! Vlada is vonuchka by the way"


async def command_start_handler(message: Message) -> None:
    await message.answer(START_MESSAGE)
