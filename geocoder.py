import aiohttp

from errors import CityNotFoundError, WeatherApiError
from models import City


class Geocoder:
    """Ищет город по названию и возвращает его координаты (Open-Meteo Geocoding API)."""

    URL = "https://geocoding-api.open-meteo.com/v1/search"

    # разговорные названия, которые api понимает неправильно (например "Питер" - это поселок в Пермском крае)
    ALIASES = {
        "питер": "Санкт-Петербург",
        "спб": "Санкт-Петербург",
        "мск": "Москва",
        "екб": "Екатеринбург",
        "нск": "Новосибирск",
    }

    def __init__(self, timeout_seconds: int = 10):
        self.timeout = aiohttp.ClientTimeout(total=timeout_seconds)

    async def find(self, name: str) -> City:
        name = name.strip()
        if not name:
            raise CityNotFoundError(name)
        query = self.ALIASES.get(name.lower(), name)

        params = {"name": query, "count": 1, "language": "ru", "format": "json"}
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(self.URL, params=params) as response:
                    if response.status != 200:
                        raise WeatherApiError()
                    data = await response.json()
        except (aiohttp.ClientError, TimeoutError):
            raise WeatherApiError()

        # если ничего не нашлось, поля results в ответе нет
        results = data.get("results")
        if not results:
            raise CityNotFoundError(name)

        item = results[0]
        return City(
            name=item["name"],
            country=item.get("country", ""),
            latitude=item["latitude"],
            longitude=item["longitude"],
        )
