import logging
import asyncio
from utils.dp import dp, bot
from utils.beautifulle_txt_to_cmd import important_b_text_to_cmd

logging.basicConfig(level=logging.INFO)

async def main():
    from handlers import start, random_question, proverka, help, new_chat_members  # импортируем все обработчики
    await dp.start_polling(bot)

if __name__ == "__main__":
    important_b_text_to_cmd(text="Бот запущен и готов к работе")
    asyncio.run(main())
