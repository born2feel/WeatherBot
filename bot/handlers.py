from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

HELP_TEXT = (
    "Я бот погоды. Что я умею:\n"
    "/city ГОРОД - запомнить ваш город\n"
    "/now [ГОРОД] - погода сейчас\n"
    "/forecast [ДНЕЙ] - прогноз на 1-7 дней\n"
    "/wear - что надеть сегодня\n"
    "/compare ГОРОД1 ГОРОД2 - сравнить погоду\n"
    "/help - эта справка"
)


class BotHandlers:
    """Обработчики команд. Каждая команда - отдельный метод, все они собираются в router."""

    def __init__(self):
        self.router = Router()
        self.router.message.register(self.start, CommandStart())
        self.router.message.register(self.help, Command("help"))

    async def start(self, message: Message):
        name = message.from_user.first_name if message.from_user else "друг"
        await message.answer(f"Привет, {name}!\n\n{HELP_TEXT}")

    async def help(self, message: Message):
        await message.answer(HELP_TEXT)
