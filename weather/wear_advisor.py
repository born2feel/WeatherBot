from weather.models import CurrentWeather

# коды WMO с дождем/моросью/грозой и со снегом
RAIN_CODES = {51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82, 95, 96, 99}
SNOW_CODES = {71, 73, 75, 77, 85, 86}
CLEAR_CODES = {0, 1}


class WearAdvisor:
    """Советует, что надеть. Смотрит на температуру по ощущениям, осадки и ветер."""

    STRONG_WIND = 10  # м/с

    def advise(self, weather: CurrentWeather) -> list[str]:
        advice = [self._clothes_for(weather.feels_like)]

        if weather.weather_code in RAIN_CODES:
            advice.append("Возьмите зонт и непромокаемую обувь")
        elif weather.weather_code in SNOW_CODES:
            advice.append("Идет снег - пригодится непромокаемая обувь")

        if weather.wind_speed >= self.STRONG_WIND:
            advice.append("Сильный ветер - лучше куртка с капюшоном, зонт может сломаться")

        if weather.temperature >= 25 and weather.weather_code in CLEAR_CODES:
            advice.append("Солнечно и жарко - не забудьте очки и воду")

        return advice

    def _clothes_for(self, feels_like: float) -> str:
        if feels_like <= -15:
            return "Очень холодно: пуховик, термобелье, шапка, шарф и варежки"
        if feels_like <= -5:
            return "Холодно: зимняя куртка, шапка и перчатки"
        if feels_like <= 5:
            return "Прохладно: теплая куртка и шапка"
        if feels_like <= 12:
            return "Свежо: демисезонная куртка или ветровка"
        if feels_like <= 18:
            return "Тепло: легкая куртка или кофта"
        if feels_like <= 24:
            return "Тепло: футболка, на вечер - легкая кофта"
        return "Жарко: футболка, шорты и кепка"
