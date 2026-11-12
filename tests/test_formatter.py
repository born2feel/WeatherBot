from datetime import date

from weather.formatter import Formatter
from weather.models import City, CurrentWeather, DayForecast

MOSCOW = City("Москва", "Россия", 55.75, 37.62)
SOCHI = City("Сочи", "Россия", 43.6, 39.73)


def make_weather(temperature):
    return CurrentWeather(temperature, temperature, 50, 3, 0, 3)


def test_current_shows_city_and_temperature():
    text = Formatter().current(MOSCOW, make_weather(-3.4))
    assert "Москва" in text
    assert "-3°" in text


def test_positive_temperature_has_plus():
    text = Formatter().current(MOSCOW, make_weather(5))
    assert "+5°" in text


def test_forecast_has_line_for_each_day():
    days = [DayForecast(date(2026, 11, 16), 1, 5, 40, 3, 61),
            DayForecast(date(2026, 11, 17), 0, 3, 10, 2, 3)]
    text = Formatter().forecast(MOSCOW, days)
    assert "16.11 пн" in text
    assert "17.11 вт" in text


def test_compare_says_which_city_is_warmer():
    text = Formatter().compare(MOSCOW, make_weather(2), SOCHI, make_weather(14))
    assert "В городе Сочи теплее на 12°" in text


def test_city_name_is_escaped():
    city = City("<b>", "", 0, 0)
    assert "&lt;b&gt;" in Formatter().city_title(city)
