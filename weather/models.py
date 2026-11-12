from dataclasses import dataclass
from datetime import date

# коды погоды WMO, которые возвращает Open-Meteo
WEATHER_CODES = {
    0: "ясно",
    1: "преимущественно ясно",
    2: "переменная облачность",
    3: "пасмурно",
    45: "туман",
    48: "изморозь",
    51: "слабая морось",
    53: "морось",
    55: "сильная морось",
    56: "ледяная морось",
    57: "сильная ледяная морось",
    61: "небольшой дождь",
    63: "дождь",
    65: "сильный дождь",
    66: "ледяной дождь",
    67: "сильный ледяной дождь",
    71: "небольшой снег",
    73: "снег",
    75: "сильный снег",
    77: "снежная крупа",
    80: "небольшой ливень",
    81: "ливень",
    82: "сильный ливень",
    85: "небольшой снегопад",
    86: "сильный снегопад",
    95: "гроза",
    96: "гроза с градом",
    99: "сильная гроза с градом",
}


def describe_weather(code: int) -> str:
    return WEATHER_CODES.get(code, "неизвестно")


@dataclass
class City:
    name: str
    country: str
    latitude: float
    longitude: float


@dataclass
class CurrentWeather:
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float  # м/с
    precipitation: float  # мм
    weather_code: int

    @property
    def description(self) -> str:
        return describe_weather(self.weather_code)


@dataclass
class DayForecast:
    day: date
    temp_min: float
    temp_max: float
    precipitation_chance: int  # %
    wind_speed: float  # м/с
    weather_code: int

    @property
    def description(self) -> str:
        return describe_weather(self.weather_code)
