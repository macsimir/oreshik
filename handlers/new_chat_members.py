from aiogram import types, F
from utils.dp import dp

@dp.message(F.new_chat_members)
async def somebody_added(message: types.Message):
    for user in message.new_chat_members:
        await message.reply(f"Привет, {user.full_name}")
