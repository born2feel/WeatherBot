class WeatherBotError(Exception):
    """Общая ошибка бота. Текст ошибки можно показать пользователю."""


class CityNotFoundError(WeatherBotError):
    def __init__(self, city_name: str):
        super().__init__(f"Город «{city_name}» не найден. Проверьте название.")


class WeatherApiError(WeatherBotError):
    def __init__(self):
        super().__init__("Сервис погоды сейчас недоступен. Попробуйте позже.")
