from abc import ABC, abstractmethod
from datetime import date

import aiohttp

from weather.errors import WeatherApiError
from weather.models import City, CurrentWeather, DayForecast


class WeatherProvider(ABC):
    """Общий контракт для источника погоды. Остальной код не знает, откуда берутся данные."""

    @abstractmethod
    async def get_current(self, city: City) -> CurrentWeather:
        pass

    @abstractmethod
    async def get_forecast(self, city: City, days: int) -> list[DayForecast]:
        pass


class OpenMeteoProvider(WeatherProvider):
    """Погода с open-meteo.com. Ключ api не нужен."""

    URL = "https://api.open-meteo.com/v1/forecast"
    MAX_DAYS = 7

    def __init__(self, timeout_seconds: int = 10):
        self.timeout = aiohttp.ClientTimeout(total=timeout_seconds)

    async def get_current(self, city: City) -> CurrentWeather:
        data = await self._request(city, {
            "current": "temperature_2m,apparent_temperature,relative_humidity_2m,"
                       "precipitation,weather_code,wind_speed_10m",
            "forecast_days": 1,
        })
        current = data["current"]
        return CurrentWeather(
            temperature=current["temperature_2m"],
            feels_like=current["apparent_temperature"],
            humidity=current["relative_humidity_2m"],
            wind_speed=current["wind_speed_10m"],
            precipitation=current["precipitation"],
            weather_code=current["weather_code"],
        )

    async def get_forecast(self, city: City, days: int) -> list[DayForecast]:
        days = max(1, min(days, self.MAX_DAYS))
        data = await self._request(city, {
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,"
                     "precipitation_probability_max,wind_speed_10m_max",
            "forecast_days": days,
        })
        # daily приходит как набор списков: daily["time"][i], daily["temperature_2m_max"][i] ...
        daily = data["daily"]
        forecast = []
        for i in range(len(daily["time"])):
            forecast.append(DayForecast(
                day=date.fromisoformat(daily["time"][i]),
                temp_min=daily["temperature_2m_min"][i],
                temp_max=daily["temperature_2m_max"][i],
                precipitation_chance=daily["precipitation_probability_max"][i] or 0,
                wind_speed=daily["wind_speed_10m_max"][i],
                weather_code=daily["weather_code"][i],
            ))
        return forecast

    async def _request(self, city: City, extra_params: dict) -> dict:
        params = {
            "latitude": city.latitude,
            "longitude": city.longitude,
            "timezone": "auto",
            "wind_speed_unit": "ms",
            **extra_params,
        }
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(self.URL, params=params) as response:
                    if response.status != 200:
                        raise WeatherApiError()
                    return await response.json()
        except (aiohttp.ClientError, TimeoutError):
            raise WeatherApiError()
