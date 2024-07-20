from aiogram import types
from aiogram.filters import Command
from utils.dp import bot, dp
from db.datebase import User, Session, get_user_by_telegram_id
from utils.config import CHANNEL_ID
from utils.beautifulle_txt_to_cmd import plain_b_text_to_cmd
from keyboard.keyboard import random_question_button

text = "Привет, Я орешек выбери режим"

@dp.message(Command("start"))
async def check_subscription(message: types.Message):
    telegram_id = message.from_user.id
    user_id = message.from_user.id

    # Создаем сессию для взаимодействия с БД
    session = Session() 

    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in ['member', 'administrator', 'creator']:
            if not User.telegram_id_exists(session, telegram_id):
                privilege = "user"
                new_user = User(telegram_id=telegram_id, privilege=privilege)
                session.add(new_user)
                session.commit()
                plain_b_text_to_cmd(text="Создан новый пользователь")
                await message.reply("Спасибо за подписку!")
                await message.answer("Привет, я орешек. Список команд /help ")
            else:
                user = get_user_by_telegram_id(session, telegram_id)  # Передаем session
                if user and user.privilege == "admin":
                    await message.answer("Привет, админ", reply_markup=random_question_button)
                else:
                    await message.answer("Еще раз привет! /random_q")
        else:
            await message.reply("Вы не подписаны на канал. Пожалуйста, подпишитесь. @testik092")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")
    finally:
        # Закрываем сессию
        session.close()
