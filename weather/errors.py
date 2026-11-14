from html import escape


class WeatherBotError(Exception):
    """Общая ошибка бота. Текст ошибки можно показать пользователю."""


class CityNotFoundError(WeatherBotError):
    def __init__(self, city_name: str):
        # название ввел пользователь, а ответ уходит с html разметкой - экранируем
        super().__init__(f"Город «{escape(city_name)}» не найден. Проверьте название.")


class WeatherApiError(WeatherBotError):
    def __init__(self):
        super().__init__("Сервис погоды сейчас недоступен. Попробуйте позже.")


class NoCityError(WeatherBotError):
    def __init__(self):
        super().__init__("Сначала укажите свой город: /city Москва\nИли напишите город прямо в команде: /now Москва")


class BadArgumentError(WeatherBotError):
    """Пользователь неправильно ввел аргументы команды. Текст подсказывает, как правильно."""
