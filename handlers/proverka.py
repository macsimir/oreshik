from aiogram import types, F
from utils.dp import dp, bot
from utils.state import Username_for_questions_for_friends
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboard.keyboard import mode_selection_proverka_keyboard
from db.datebase import Session, Lobby_for_questions

@dp.callback_query(F.data == "questions_for_friends_F_key")
async def questions_for_friends_F_funck(callback: types.CallbackQuery, state: FSMContext):
    chat_id = callback.message.chat.id
    # Call the function to get the keyboard instance
    await callback.message.answer(f"Создайте или зайдите в лобби", reply_markup=mode_selection_proverka_keyboard())

@dp.callback_query(F.data == "create_to_lobby_F_key")
async def create_to_lobby_F_key_funck(callback: types.CallbackQuery, state: FSMContext):
    session = Session()
    user_id = callback.message.chat.id
    name_user = callback.message.from_user.first_name
    new_lobby = Lobby_for_questions(lobby_creator_id=user_id,lobby_creator_name= name_user)
    # You may need to add new_lobby to the session and commit
    session.add(new_lobby)
    session.commit()
    await callback.message.answer('Лобби создано, Ждите пока кто то добавится в ваш лобби')

@dp.callback_query(F.data == "connect_to_lobby_F_key")
async def connect_to_lobby_F_key_funck(callback: types.CallbackQuery, state: FSMContext):
    session = Session()
    lobby = session.query(Lobby_for_questions).all()
    if lobby:
        for i in lobby:
            await callback.message.answer(f"""
        Выбирите лобби:
        Лобби №{i.id_lobby}:
        Создатель - {i.lobby_creator_name}""")
    else:
        await callback.message.answer(f"Не одно лобби в чате нету ")        