from aiogram import types
from aiogram.filters import Command
from utils.dp import dp

@dp.message(Command("proverka"))
async def proverka_command_funck(message: types.Message):
    await message.answer("Это режим для проверки знания друг друга \n Для того чтобы начать ввидите ник пользователя")
