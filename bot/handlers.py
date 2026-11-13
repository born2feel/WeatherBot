import logging
from html import escape

from aiogram import F, Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import CallbackQuery, Message

from bot.keyboards import (BUTTON_FORECAST, BUTTON_HELP, BUTTON_NOW, BUTTON_WEAR, FORECAST_CALLBACK,
                           forecast_days_keyboard, main_keyboard)
from weather.errors import WeatherBotError
from weather.service import WeatherService

HELP_TEXT = (
    "Я бот погоды. Что я умею:\n"
    "/city ГОРОД - запомнить ваш город\n"
    "/now [ГОРОД] - погода сейчас\n"
    "/forecast [ДНЕЙ] - прогноз на 1-7 дней\n"
    "/wear [ГОРОД] - что надеть\n"
    "/compare ГОРОД1 ГОРОД2 - сравнить погоду\n"
    "/help - эта справка\n\n"
    "Города из нескольких слов в /compare пишите через запятую: /compare Москва, Нижний Новгород"
)

logger = logging.getLogger(__name__)


class BotHandlers:
    """Обработчики телеграма. Достают из сообщения аргументы, вызывают WeatherService и отправляют ответ."""

    def __init__(self, service: WeatherService):
        self._service = service
        self.router = Router()

        self.router.message.register(self.start, CommandStart())
        self.router.message.register(self.help, Command("help"))
        self.router.message.register(self.help, F.text == BUTTON_HELP)
        self.router.message.register(self.city, Command("city"))
        self.router.message.register(self.now, Command("now"))
        self.router.message.register(self.now_button, F.text == BUTTON_NOW)
        self.router.message.register(self.forecast, Command("forecast"))
        self.router.message.register(self.forecast_button, F.text == BUTTON_FORECAST)
        self.router.message.register(self.wear, Command("wear"))
        self.router.message.register(self.wear_button, F.text == BUTTON_WEAR)
        self.router.message.register(self.compare, Command("compare"))
        self.router.callback_query.register(self.forecast_days, F.data.startswith(FORECAST_CALLBACK))
        # последним - все остальное, что не подошло под команды выше
        self.router.message.register(self.unknown)

    async def start(self, message: Message):
        name = escape(message.from_user.first_name) if message.from_user else "друг"
        await message.answer(f"Привет, {name}!\n\n{HELP_TEXT}", reply_markup=main_keyboard())

    async def help(self, message: Message):
        await message.answer(HELP_TEXT, reply_markup=main_keyboard())

    async def city(self, message: Message, command: CommandObject):
        await self._answer(message, self._service.set_city(message.from_user.id, command.args or ""))

    async def now(self, message: Message, command: CommandObject):
        await self._answer(message, self._service.now(message.from_user.id, command.args or ""))

    async def now_button(self, message: Message):
        await self._answer(message, self._service.now(message.from_user.id))

    async def forecast(self, message: Message, command: CommandObject):
        await self._answer(message, self._service.forecast(message.from_user.id, command.args or ""),
                           forecast_days_keyboard())

    async def forecast_button(self, message: Message):
        await self._answer(message, self._service.forecast(message.from_user.id), forecast_days_keyboard())

    async def wear(self, message: Message, command: CommandObject):
        await self._answer(message, self._service.wear(message.from_user.id, command.args or ""))

    async def wear_button(self, message: Message):
        await self._answer(message, self._service.wear(message.from_user.id))

    async def compare(self, message: Message, command: CommandObject):
        await self._answer(message, self._service.compare(message.from_user.id, command.args or ""))

    async def forecast_days(self, callback: CallbackQuery):
        """Нажатие inline-кнопки 1/3/7 дней под прогнозом - меняем текст того же сообщения."""
        days = callback.data.removeprefix(FORECAST_CALLBACK)
        try:
            text = await self._service.forecast(callback.from_user.id, days)
        except WeatherBotError as e:
            await callback.answer(str(e), show_alert=True)
            return
        if callback.message and callback.message.text != text:
            await callback.message.edit_text(text, reply_markup=forecast_days_keyboard())
        await callback.answer()

    async def unknown(self, message: Message):
        if message.text:
            await message.answer("Не понял команду. Посмотрите /help")
        else:
            await message.answer("Я понимаю только текстовые команды. Посмотрите /help")

    async def _answer(self, message: Message, service_call, keyboard=None):
        """Общая обработка ошибок для всех команд: бот не должен падать ни на каком вводе."""
        try:
            text = await service_call
        except WeatherBotError as e:
            text = str(e)
            keyboard = None
        except Exception:
            logger.exception("Ошибка при обработке сообщения %r", message.text)
            text = "Что-то пошло не так. Попробуйте еще раз."
            keyboard = None
        await message.answer(text, reply_markup=keyboard)
