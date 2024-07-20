from aiogram import types
from aiogram.filters import Command
from utils.dp import dp

@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer("""Список комманд: \n /random_q""")
