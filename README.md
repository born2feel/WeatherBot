# WeatherBot

laboratory work 4 OOP

Telegram-бот погоды. Показывает погоду сейчас и прогноз на несколько дней, советует, что надеть, сравнивает погоду в двух городах. Город пользователя запоминается, поэтому его не нужно вводить каждый раз.

Данные о погоде берутся из [Open-Meteo](https://open-meteo.com/) — ключ API не нужен.

## Команды
| Команда | Что делает |
|---|---|
| `/start`, `/help` | приветствие и справка, кнопки под полем ввода |
| `/city ГОРОД` | запомнить свой город (`/city Москва`, понимает `Питер`, `СПб`, `Мск`) |
| `/now [ГОРОД]` | погода сейчас: температура, ощущается как, ветер, влажность |
| `/forecast [ДНЕЙ]` | прогноз на 1–7 дней (по умолчанию 3), под ним кнопки 1 / 3 / 7 дней |
| `/wear [ГОРОД]` | что надеть с учетом температуры, осадков и ветра |
| `/compare ГОРОД1 ГОРОД2` | сравнить погоду; с одним городом — сравнение со своим. Города из нескольких слов через запятую: `/compare Москва, Нижний Новгород` |

На любой неправильный ввод (неизвестный город, `/forecast abc`, нет интернета, стикер вместо текста) бот отвечает понятным сообщением и продолжает работать.

## Запуск
1. Создать бота у [@BotFather](https://t.me/BotFather) командой `/newbot` и получить токен
2. Скопировать `.env.example` в `.env` и вписать токен: `BOT_TOKEN=...`
3. Установить зависимости и запустить:
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Тесты: `pytest`

## Структура
```
main.py              запуск, сборка объектов
config.py            Config - токен из .env
bot/
  handlers.py        BotHandlers - команды и кнопки телеграма
  keyboards.py       reply и inline кнопки
weather/
  service.py         WeatherService - логика всех команд
  provider.py        WeatherProvider (абстрактный класс) и OpenMeteoProvider
  geocoder.py        Geocoder - название города -> координаты
  wear_advisor.py    WearAdvisor - что надеть
  formatter.py       Formatter - текст ответов
  models.py          City, CurrentWeather, DayForecast
  errors.py          свои исключения
storage/
  user_storage.py    UserStorage - города пользователей в users.json
tests/               тесты на pytest
```

Пакет `weather` ничего не знает о Telegram: `bot` только принимает сообщения и передает их в `WeatherService`.

## Технологии
Python 3.13, aiogram 3, aiohttp, python-dotenv, pytest
