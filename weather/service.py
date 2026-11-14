from storage.user_storage import UserStorage
from weather.errors import BadArgumentError, NoCityError
from weather.formatter import Formatter
from weather.geocoder import Geocoder
from weather.models import City
from weather.provider import WeatherProvider
from weather.wear_advisor import WearAdvisor


class WeatherService:
    """Логика всех команд бота. Принимает текст аргументов, возвращает готовый ответ.
    О телеграме ничего не знает - его можно подключить к любому мессенджеру."""

    DEFAULT_DAYS = 3

    def __init__(self, geocoder: Geocoder, provider: WeatherProvider, storage: UserStorage,
                 advisor: WearAdvisor, formatter: Formatter):
        self._geocoder = geocoder
        self._provider = provider
        self._storage = storage
        self._advisor = advisor
        self._formatter = formatter

    async def set_city(self, user_id: int, city_name: str) -> str:
        if not city_name.strip():
            raise BadArgumentError("Напишите город после команды, например: /city Москва")
        city = await self._geocoder.find(city_name)
        self._storage.set_city(user_id, city)
        return f"Запомнил: {self._formatter.city_title(city)}\nТеперь можно просто писать /now, /forecast, /wear"

    async def now(self, user_id: int, city_name: str = "") -> str:
        city = await self._resolve_city(user_id, city_name)
        weather = await self._provider.get_current(city)
        return self._formatter.current(city, weather)

    async def forecast(self, user_id: int, days_text: str = "") -> str:
        days = self._parse_days(days_text)
        city = await self._resolve_city(user_id, "")
        forecast = await self._provider.get_forecast(city, days)
        return self._formatter.forecast(city, forecast)

    async def wear(self, user_id: int, city_name: str = "") -> str:
        city = await self._resolve_city(user_id, city_name)
        weather = await self._provider.get_current(city)
        advice = self._advisor.advise(weather)
        return self._formatter.wear(city, weather, advice)

    async def compare(self, user_id: int, args: str) -> str:
        names = self._split_cities(args)
        if len(names) == 1:
            # один город - сравниваем с городом пользователя
            first = await self._resolve_city(user_id, "")
            second = await self._geocoder.find(names[0])
        else:
            first = await self._geocoder.find(names[0])
            second = await self._geocoder.find(names[1])

        weather1 = await self._provider.get_current(first)
        weather2 = await self._provider.get_current(second)
        return self._formatter.compare(first, weather1, second, weather2)

    async def _resolve_city(self, user_id: int, city_name: str) -> City:
        """Город из команды, а если его нет - сохраненный город пользователя."""
        if city_name.strip():
            return await self._geocoder.find(city_name)
        city = self._storage.get_city(user_id)
        if city is None:
            raise NoCityError()
        return city

    def _parse_days(self, text: str) -> int:
        text = text.strip()
        if not text:
            return self.DEFAULT_DAYS
        if not text.isdigit() or not 1 <= int(text) <= 7:
            raise BadArgumentError("Количество дней - число от 1 до 7, например: /forecast 5")
        return int(text)

    def _split_cities(self, args: str) -> list[str]:
        # города через запятую, чтобы работали названия из нескольких слов: /compare Москва, Нижний Новгород
        if "," in args:
            names = [name.strip() for name in args.split(",")]
        else:
            names = args.split()
        names = [name for name in names if name]

        if not 1 <= len(names) <= 2:
            raise BadArgumentError(
                "Укажите один или два города:\n/compare Сочи\n/compare Москва Сочи\n"
                "/compare Москва, Нижний Новгород"
            )
        return names
