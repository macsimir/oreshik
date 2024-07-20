from aiogram import types,F
from aiogram.filters import Command
from utils.dp import dp
from db.datebase import User, Question, UserQuestion, Session
import random



@dp.message(F.text.lower() == "с пюрешкой")
async def cmd_random_question_funck(message:types.Message):
    session = Session()
    user_telegram_id = message.chat.id

    user = session.query(User).filter_by(telegram_id=user_telegram_id).first()
    
    if not user:    
        await message.answer("Сначала зарегистрируйтесь, отправив команду /start")
        session.close()
        return

    max_question_id = session.query(Question).count()
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




@dp.message(Command("r"))
async def cmd_random_question(message: types.Message):
    session = Session()
    user_telegram_id = message.chat.id

    user = session.query(User).filter_by(telegram_id=user_telegram_id).first()
    
    if not user:    
        await message.answer("Сначала зарегистрируйтесь, отправив команду /start")
        session.close()
        return

    max_question_id = session.query(Question).count()
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
