from aiogram.types import Message


async def open_debt_menu(message: Message) -> None:
    await message.answer('Приложение "Долги"')
