import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from bot.handlers import BotHandlers
from config import Config
from storage.user_storage import UserStorage
from weather.formatter import Formatter
from weather.geocoder import Geocoder
from weather.provider import OpenMeteoProvider
from weather.service import WeatherService
from weather.wear_advisor import WearAdvisor

COMMANDS = [
    BotCommand(command="now", description="Погода сейчас"),
    BotCommand(command="forecast", description="Прогноз на несколько дней"),
    BotCommand(command="wear", description="Что надеть"),
    BotCommand(command="city", description="Запомнить мой город"),
    BotCommand(command="compare", description="Сравнить два города"),
    BotCommand(command="help", description="Справка"),
]


async def main():
    logging.basicConfig(level=logging.INFO)

    config = Config()

    # собираем объекты здесь, классы сами не создают свои зависимости
    service = WeatherService(
        geocoder=Geocoder(),
        provider=OpenMeteoProvider(),
        storage=UserStorage(),
        advisor=WearAdvisor(),
        formatter=Formatter(),
    )

    bot = Bot(token=config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dispatcher = Dispatcher()
    dispatcher.include_router(BotHandlers(service).router)

    await bot.set_my_commands(COMMANDS)  # меню команд в телеграме
    print("Бот запущен. Остановить - Ctrl+C")
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except ValueError as e:
        print("Ошибка:", e)
    except KeyboardInterrupt:
        print("Бот остановлен.")
