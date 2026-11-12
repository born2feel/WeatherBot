from html import escape

from weather.models import City, CurrentWeather, DayForecast

WEEKDAYS = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]


def weather_emoji(code: int) -> str:
    if code == 0:
        return "☀️"
    if code in (1, 2):
        return "🌤"
    if code == 3:
        return "☁️"
    if code in (45, 48):
        return "🌫"
    if code in (71, 73, 75, 77, 85, 86):
        return "❄️"
    if code >= 95:
        return "⛈"
    return "🌧"


class Formatter:
    """Собирает текст ответа для пользователя (HTML разметка телеграма)."""

    def city_title(self, city: City) -> str:
        # название приходит из api, экранируем на всякий случай
        title = escape(city.name)
        if city.country:
            title += f", {escape(city.country)}"
        return f"<b>{title}</b>"

    def current(self, city: City, weather: CurrentWeather) -> str:
        return (
            f"{self.city_title(city)}\n"
            f"{weather_emoji(weather.weather_code)} {weather.description.capitalize()}\n"
            f"🌡 {self._temp(weather.temperature)}, ощущается как {self._temp(weather.feels_like)}\n"
            f"💨 Ветер {weather.wind_speed:.1f} м/с\n"
            f"💧 Влажность {weather.humidity}%"
        )

    def forecast(self, city: City, days: list[DayForecast]) -> str:
        lines = [f"{self.city_title(city)} - прогноз на {len(days)} дн."]
        for day in days:
            lines.append(
                f"{day.day.strftime('%d.%m')} {WEEKDAYS[day.day.weekday()]} "
                f"{weather_emoji(day.weather_code)} {self._temp(day.temp_min)}..{self._temp(day.temp_max)}, "
                f"{day.description}, осадки {day.precipitation_chance}%"
            )
        return "\n".join(lines)

    def wear(self, city: City, weather: CurrentWeather, advice: list[str]) -> str:
        lines = [
            f"{self.city_title(city)}: {self._temp(weather.temperature)}, {weather.description}",
            "",
            "👕 Что надеть:",
        ]
        lines += [f"• {item}" for item in advice]
        return "\n".join(lines)

    def compare(self, city1: City, weather1: CurrentWeather, city2: City, weather2: CurrentWeather) -> str:
        # сравниваем округленные значения, чтобы разница совпадала с тем, что видит пользователь
        diff = round(weather1.temperature) - round(weather2.temperature)
        if diff == 0:
            verdict = "Температура одинаковая"
        elif diff > 0:
            verdict = f"В городе {escape(city1.name)} теплее на {diff}°"
        else:
            verdict = f"В городе {escape(city2.name)} теплее на {-diff}°"

        return (
            f"{self.city_title(city1)}: {weather_emoji(weather1.weather_code)} "
            f"{self._temp(weather1.temperature)}, {weather1.description}, ветер {weather1.wind_speed:.1f} м/с\n"
            f"{self.city_title(city2)}: {weather_emoji(weather2.weather_code)} "
            f"{self._temp(weather2.temperature)}, {weather2.description}, ветер {weather2.wind_speed:.1f} м/с\n\n"
            f"{verdict}"
        )

    def _temp(self, value: float) -> str:
        value = round(value)
        return f"+{value}°" if value > 0 else f"{value}°"
