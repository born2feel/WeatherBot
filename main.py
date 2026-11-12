import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import Config
from bot.handlers import BotHandlers


async def main():
    logging.basicConfig(level=logging.INFO)

    config = Config()
    bot = Bot(token=config.bot_token)
    dispatcher = Dispatcher()
    dispatcher.include_router(BotHandlers().router)

    print("Бот запущен. Остановить - Ctrl+C")
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except ValueError as e:
        print("Ошибка:", e)
    except KeyboardInterrupt:
        print("Бот остановлен.")
