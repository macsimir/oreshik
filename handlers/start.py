from aiogram import types
from aiogram.filters import Command
from utils.dp import bot, dp
from db.datebase import User, Session, get_user_by_telegram_id
from utils.config import CHANNEL_ID
from utils.beautifulle_txt_to_cmd import plain_b_text_to_cmd
from keyboard.keyboard import random_question_button, mode_selection_start_keyboard


@dp.message(Command("start"))
async def check_subscription(message: types.Message):
    first_name = message.from_user.first_name 
    telegram_id = message.from_user.id
    user_id = message.from_user.id
    text_to_start = f"Привет {first_name}, Я орешек выбери режим работы "


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
                await message.reply("Спасибо за подписку!")
                await message.answer(first_name, reply_markup=mode_selection_start_keyboard())
            else:
                user = get_user_by_telegram_id(session, telegram_id)  # Передаем session
                if user and user.privilege == "admin":
                    await message.answer(f"Привет, админ {first_name}", reply_markup=random_question_button())
                else:
                    await message.answer(text_to_start, reply_markup=mode_selection_start_keyboard())
        else:
            await message.reply("Вы не подписаны на канал. Пожалуйста, подпишитесь. @testik092")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")
    finally:
        # Закрываем сессию
        session.close()
