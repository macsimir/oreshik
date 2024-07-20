from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from db import User, Question, UserQuestion, Session
import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO)
bot = Bot(token="6449820894:AAHzMs00mCfo3H1dYKFdJXz_csn7__q5ReE")
dp = Dispatcher()
CHANNEL_ID = "@testik092"

@dp.message(Command("start"))
async def check_subscription(message: types.Message):
    telegram_id = message.from_user.id
    session = Session() 
    user_id = message.from_user.id
    try: 
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in ['member', 'administrator', 'creator']:
            if not User.telegram_id_exists(session, telegram_id):
                privilege = "admin"
                new_user = User(telegram_id=telegram_id, privilege=privilege)
                session.add(new_user)
                session.commit()
                await message.reply("Спасибо за подписку!")
                await message.answer("Привет, я орешек. Список комманд /help ")
            else:
                await message.answer('Еще раз привет! /random_q')
        else:
            await message.reply("Вы не подписаны на канал. Пожалуйста, подпишитесь.@testik092")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")


@dp.message(Command("random_q"))
async def cmd_random_question(message: types.Message):
    session = Session()
    user_telegram_id = message.from_user.id

    # Получаем объект пользователя из БД
    user = session.query(User).filter_by(telegram_id=user_telegram_id).first()
    
    if not user:
        await message.answer("Сначала зарегистрируйтесь, отправив команду /start")
        session.close()
        return

    max_question_id = session.query(Question).count()
    question = None
    user_question = None

    while not question or user_question:
        question_id = random.randint(1, max_question_id)  # Измените диапазон в соответствии с количеством вопросов в вашей БД
        question = session.query(Question).filter_by(question_id=question_id).first()
        
        if question:
            # Проверяем, показывался ли уже этот вопрос пользователю
            user_question = session.query(UserQuestion).filter_by(user_id=user.user_id, question_id=question_id).first()

    # Если мы нашли новый вопрос, сохраняем его в таблицу UserQuestion
    user_question = UserQuestion(user_id=user.user_id, question_id=question_id, asked=True)
    session.add(user_question)
    session.commit()
    await message.answer(question.question_text)
    
    session.close()

@dp.message(Command("help","command"))
async def help_command(message: types.Message):
    await message.answer("""Список комманд: \n /random_q""")


# @dp.message(F.new_chat_members)
# async def somebody_added(message: Message):
#     for user in message.new_chat_members:
#         # проперти full_name берёт сразу имя И фамилию 
#         # (на скриншоте выше у юзеров нет фамилии)
#         await message.reply(f"Привет, {user.full_name}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("Бот запущен и готов к работе")
    asyncio.run(main())
