from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

# текст на кнопках - по нему handlers понимают, какая кнопка нажата
BUTTON_NOW = "🌡 Погода сейчас"
BUTTON_FORECAST = "📅 Прогноз"
BUTTON_WEAR = "👕 Что надеть"
BUTTON_HELP = "❓ Помощь"

FORECAST_CALLBACK = "forecast:"


def main_keyboard() -> ReplyKeyboardMarkup:
    """Кнопки под полем ввода, 2 в ряд."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BUTTON_NOW), KeyboardButton(text=BUTTON_FORECAST)],
            [KeyboardButton(text=BUTTON_WEAR), KeyboardButton(text=BUTTON_HELP)],
        ],
        resize_keyboard=True,
    )


def forecast_days_keyboard() -> InlineKeyboardMarkup:
    """Кнопки под сообщением с прогнозом: выбрать количество дней."""
    buttons = [
        InlineKeyboardButton(text=f"{days} дн.", callback_data=f"{FORECAST_CALLBACK}{days}")
        for days in (1, 3, 7)
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])
