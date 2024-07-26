from aiogram import types, F
from utils.dp import dp, bot
from utils.state import Username_for_questions_for_friends
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboard.keyboard import mode_selection_proverka_keyboard, connect_to_lobby_choice_keyboard
from db.datebase import Session, Lobby_for_questions, Questions_for_each_other, Questions_for_each_other_Lobby
import random 
import logging

MAX_LOBBIES = 2  # Максимальное количество лобби

@dp.callback_query(F.data == "questions_for_friends_F_key")
async def questions_for_friends_F_funck(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Создайте или зайдите в лобби", reply_markup=mode_selection_proverka_keyboard())
    await callback.message.edit_reply_markup(reply_markup=None) 

@dp.callback_query(F.data == "create_to_lobby_F_key")
async def create_to_lobby_F_key_funck(callback: types.CallbackQuery, state: FSMContext):
    session = Session()
    user_id = callback.from_user.id
    name_user = callback.from_user.first_name
    
    # Проверка на наличие лобби от этого пользователя
    existing_lobby = session.query(Lobby_for_questions).filter_by(lobby_creator_id=user_id).first()
    if existing_lobby:
        await callback.message.answer('Вы уже создали лобби. Дождитесь пока кто-то добавится.')
        return
    
    # Проверка на максимальное количество лобби
    lobby_count = session.query(Lobby_for_questions).count()
    if lobby_count >= MAX_LOBBIES:
        await callback.message.answer('Достигнуто максимальное количество лобби. Пожалуйста, попробуйте позже.')
        return
    
    new_lobby = Lobby_for_questions(lobby_creator_id=user_id, lobby_creator_name=name_user, created_or_uncreated=0)
    session.add(new_lobby)
    session.commit()
    await callback.message.answer('Лобби создано. Ждите пока кто-то добавится в ваше лобби.')

@dp.callback_query(F.data == "connect_to_lobby_F_key")
async def connect_to_lobby_F_key_funck(callback: types.CallbackQuery, state: FSMContext):
    session = Session()
    lobbies = session.query(Lobby_for_questions).all()

    if lobbies:
        keyboard_builder = InlineKeyboardBuilder()
        for lobby in lobbies:
            keyboard_builder.add(
                InlineKeyboardButton(
                    text=f"Лобби №{lobby.id_lobby}: Создатель - {lobby.lobby_creator_name}",
                    callback_data=f"join_lobby_{lobby.id_lobby}"
                )
            )
        keyboard = keyboard_builder.as_markup()
        await callback.message.answer("Выберите лобби:", reply_markup=keyboard)
        await callback.message.edit_reply_markup(reply_markup=None) 
    else:
        await callback.message.answer("Нет доступных лобби в чате.")
        

@dp.callback_query(lambda c: c.data and c.data.startswith('join_lobby_'))
async def lobby_fucnk(callback: types.CallbackQuery):
    session = Session()  # Correctly create a session instance
    data = callback.data
    lobby_id = int(data.split('_')[-1])
    lobby = session.query(Lobby_for_questions).filter_by(id_lobby=lobby_id).first()
    if lobby:
        name_user = callback.from_user.first_name
        lobby.second_user_id = callback.from_user.id
        lobby.created_or_uncreated = 1
        session.commit()
        keyboard_builder = InlineKeyboardBuilder()
        keyboard_builder.add(
                InlineKeyboardButton(
                    text="Начать",
                    callback_data=f"go_to_lobby_F_key"
                )
            )
        keyboard = keyboard_builder.as_markup()
        await callback.message.answer(f"Вы зашли в лобби №{lobby.id_lobby}", reply_markup=keyboard)
    else:
        await callback.message.answer("Лобби не найдено.")


@dp.callback_query(F.data == "go_to_lobby_F_key")
async def go_to_lobby_F_key(callback: types.CallbackQuery):
    logging.info("Callback received")

    session = Session()
    user_telegram_id = callback.from_user.id
    logging.info(f"User Telegram ID: {user_telegram_id}")

    user = session.query(Lobby_for_questions).filter_by(lobby_creator_id=user_telegram_id).first()
    if not user:
        logging.error("User not found in Lobby_for_questions")
        await callback.message.answer("Ошибка: пользователь не найден.")
        session.close()
        return

    max_question_id = session.query(Questions_for_each_other).count()
    logging.info(f"Max Question ID: {max_question_id}")

    if max_question_id == 0:
        await callback.message.answer("Нет доступных вопросов.")
        session.close()
        return

    question = None
    user_question = None
    lobby_creator_id = user.lobby_creator_id
    second_user_id = user.second_user_id

    logging.info(f"Lobby Creator ID: {lobby_creator_id}, Second User ID: {second_user_id}")

    while not question or user_question:
        question_id = random.randint(1, max_question_id)
        logging.info(f"Selected Question ID: {question_id}")

        question = session.query(Questions_for_each_other).filter_by(question_id=question_id).first()
        if question:
            logging.info(f"Question Found: {question.question_text}")
            user_question = session.query(Questions_for_each_other_Lobby).filter_by(lobby_id=user.id_lobby, question_id=question_id).first()
            if user_question:
                logging.info(f"Question {question_id} already asked in lobby {user.id_lobby}")

    user_question = Questions_for_each_other_Lobby(lobby_id=user.id_lobby, question_id=question_id, asked=True)
    session.add(user_question)
    session.commit()

    await callback.bot.send_message(chat_id=lobby_creator_id, text=question.question_text)
    await callback.bot.send_message(chat_id=second_user_id, text=question.question_text)

    logging.info("Messages sent")
    session.close()