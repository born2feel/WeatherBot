import asyncio
from datetime import date, timedelta

import pytest

from storage.user_storage import UserStorage
from weather.errors import BadArgumentError, CityNotFoundError, NoCityError
from weather.formatter import Formatter
from weather.geocoder import Geocoder
from weather.models import City, CurrentWeather, DayForecast
from weather.provider import WeatherProvider
from weather.service import WeatherService
from weather.wear_advisor import WearAdvisor

CITIES = {
    "москва": City("Москва", "Россия", 55.75, 37.62),
    "сочи": City("Сочи", "Россия", 43.6, 39.73),
    "нижний новгород": City("Нижний Новгород", "Россия", 56.33, 44.0),
}
TEMPERATURES = {"Москва": 2, "Сочи": 14, "Нижний Новгород": 0}


class FakeGeocoder(Geocoder):
    """Без интернета: ищет город в словаре."""

    async def find(self, name: str) -> City:
        city = CITIES.get(name.strip().lower())
        if city is None:
            raise CityNotFoundError(name)
        return city


class FakeProvider(WeatherProvider):
    """Подменяет Open-Meteo - сервис работает с ним так же, потому что зависит только от WeatherProvider."""

    async def get_current(self, city: City) -> CurrentWeather:
        t = TEMPERATURES[city.name]
        return CurrentWeather(t, t - 3, 80, 4, 0, 3)

    async def get_forecast(self, city: City, days: int) -> list[DayForecast]:
        start = date(2026, 11, 16)
        return [DayForecast(start + timedelta(days=i), 0, 5, 50, 3, 61) for i in range(days)]


@pytest.fixture
def service(tmp_path):
    storage = UserStorage(str(tmp_path / "users.json"))
    return WeatherService(FakeGeocoder(), FakeProvider(), storage, WearAdvisor(), Formatter())


def run(coroutine):
    return asyncio.run(coroutine)


def test_now_without_city_asks_to_set_it(service):
    with pytest.raises(NoCityError):
        run(service.now(1))


def test_city_is_remembered(service):
    run(service.set_city(1, "Москва"))
    assert "Москва" in run(service.now(1))


def test_now_with_city_in_command(service):
    assert "Сочи" in run(service.now(1, "сочи"))


def test_unknown_city(service):
    with pytest.raises(CityNotFoundError):
        run(service.set_city(1, "Абвгд"))


def test_forecast_default_three_days(service):
    run(service.set_city(1, "Москва"))
    text = run(service.forecast(1))
    assert "16.11" in text and "18.11" in text and "19.11" not in text


@pytest.mark.parametrize("bad", ["0", "8", "abc", "-1"])
def test_forecast_bad_days(service, bad):
    run(service.set_city(1, "Москва"))
    with pytest.raises(BadArgumentError):
        run(service.forecast(1, bad))


def test_compare_two_cities(service):
    assert "Сочи теплее на 12°" in run(service.compare(1, "Москва Сочи"))


def test_compare_city_names_with_spaces(service):
    assert "Москва теплее на 2°" in run(service.compare(1, "Москва, Нижний Новгород"))


def test_compare_with_saved_city(service):
    run(service.set_city(1, "Сочи"))
    assert "Сочи теплее на 12°" in run(service.compare(1, "Москва"))


def test_compare_without_arguments(service):
    with pytest.raises(BadArgumentError):
        run(service.compare(1, ""))


def test_wear(service):
    text = run(service.wear(1, "Москва"))
    assert "Что надеть" in text
