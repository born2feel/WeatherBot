from storage.user_storage import UserStorage
from weather.models import City

SPB = City("Санкт-Петербург", "Россия", 59.94, 30.31)


def test_unknown_user_has_no_city(tmp_path):
    storage = UserStorage(str(tmp_path / "users.json"))
    assert storage.get_city(1) is None


def test_city_is_saved_to_file(tmp_path):
    path = str(tmp_path / "users.json")
    UserStorage(path).set_city(1, SPB)
    # новый объект читает тот же файл - как после перезапуска бота
    assert UserStorage(path).get_city(1) == SPB


def test_broken_file_does_not_crash(tmp_path):
    path = tmp_path / "users.json"
    path.write_text("{broken", encoding="utf-8")
    assert UserStorage(str(path)).get_city(1) is None
