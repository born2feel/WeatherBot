import os

from dotenv import load_dotenv


class Config:
    """Настройки бота. Токен берется из файла .env, в коде его хранить нельзя."""

    def __init__(self):
        load_dotenv()
        self.bot_token = os.getenv("BOT_TOKEN", "").strip()

        if not self.bot_token:
            raise ValueError("Не найден BOT_TOKEN. Создайте файл .env по примеру .env.example")
