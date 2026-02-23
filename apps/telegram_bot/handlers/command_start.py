from aiogram.types import Message


async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, my name is Roma!! Vlada is vonuchka by the way")
