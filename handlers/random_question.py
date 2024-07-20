from aiogram import types,F
from aiogram.filters import Command
from utils.dp import dp
from db.datebase import User, Question, UserQuestion, Session
from keyboard.keyboard import random_question_button
import random

from aiogram.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types


@dp.callback_query(F.data == "random_questions_F_key")
async def random_questions_F_funck(callback: types.CallbackQuery):
    await callback.message.answer("Режим 'Случайные вопросы' выбран" , reply_markup=random_question_button())
    


@dp.message(F.text.lower() == "новый вопрос")
async def random_questions_F_funck(message: types.Message):
    session = Session()
    user_telegram_id = message.chat.id

    user = session.query(User).filter_by(telegram_id=user_telegram_id).first()
    


    max_question_id = session.query(Question).count()
    
    if max_question_id == 0:
        await message.answer("Нет доступных вопросов.")
        session.close()
        return

    question = None
    user_question = None

    while not question or user_question:
        question_id = random.randint(1, max_question_id)
        question = session.query(Question).filter_by(question_id=question_id).first()
        
        if question:
            user_question = session.query(UserQuestion).filter_by(user_id=user.user_id, question_id=question_id).first()

    user_question = UserQuestion(user_id=user.user_id, question_id=question_id, asked=True)
    session.add(user_question)
    session.commit()
    await message.answer(question.question_text)
    
    session.close()


