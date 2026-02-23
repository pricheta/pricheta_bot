from aiogram.types import CallbackQuery


async def open_debt_menu(callback: CallbackQuery) -> None:
    await callback.message.answer('Открываю учёт долгов...')  # type: ignore
    await callback.answer()
