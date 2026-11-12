import json
import os

from weather.models import City


class UserStorage:
    """Запоминает город каждого пользователя. Данные хранятся в json файле, чтобы не терялись при перезапуске."""

    def __init__(self, file_path: str = "users.json"):
        self._file_path = file_path
        self._cities = self._load()

    def get_city(self, user_id: int) -> City | None:
        data = self._cities.get(str(user_id))  # в json ключи всегда строки
        if data is None:
            return None
        return City(**data)

    def set_city(self, user_id: int, city: City):
        self._cities[str(user_id)] = {
            "name": city.name,
            "country": city.country,
            "latitude": city.latitude,
            "longitude": city.longitude,
        }
        self._save()

    def _load(self) -> dict:
        if not os.path.exists(self._file_path):
            return {}
        try:
            with open(self._file_path, encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            # если файл испорчен, начинаем с пустого списка, а не падаем
            return {}

    def _save(self):
        with open(self._file_path, "w", encoding="utf-8") as file:
            json.dump(self._cities, file, ensure_ascii=False, indent=2)
