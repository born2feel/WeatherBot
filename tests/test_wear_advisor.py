from weather.models import CurrentWeather
from weather.wear_advisor import WearAdvisor


def make_weather(temperature=10, feels_like=10, wind_speed=2, weather_code=0):
    return CurrentWeather(temperature, feels_like, 50, wind_speed, 0, weather_code)


def test_very_cold():
    advice = WearAdvisor().advise(make_weather(temperature=-20, feels_like=-25))
    assert "пуховик" in advice[0]


def test_hot_and_sunny():
    advice = WearAdvisor().advise(make_weather(temperature=30, feels_like=31, weather_code=0))
    assert "шорты" in advice[0]
    assert any("очки" in item for item in advice)


def test_rain_needs_umbrella():
    advice = WearAdvisor().advise(make_weather(weather_code=63))
    assert any("зонт" in item for item in advice)


def test_strong_wind():
    advice = WearAdvisor().advise(make_weather(wind_speed=15))
    assert any("ветер" in item for item in advice)


def test_normal_weather_has_one_advice():
    advice = WearAdvisor().advise(make_weather(temperature=15, feels_like=15, weather_code=2))
    assert len(advice) == 1
