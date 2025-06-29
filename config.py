import os

# 🔐 Переменные окружения
TG_TOKEN = os.getenv("TG_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 👥 Список разрешённых пользователей (укажи свой Telegram ID)
ALLOWED_USERS = [
    5874151668,  # ← твой Telegram ID
]

# 📁 Пути к JSON-файлам
BASE_PATH = "data"

INGREDIENTS_FILE = os.path.join(BASE_PATH, "ingredients.json")
MINIMUMS_FILE = os.path.join(BASE_PATH, "minimums.json")
HISTORY_FILE = os.path.join(BASE_PATH, "history.json")
RECIPE_FILE = os.path.join(BASE_PATH, "recipe.json")

# 📉 Минимальные значения по умолчанию
DEFAULT_MINIMUMS = {
    "борошно": 5,
    "сіль": 1,
    "вода": 10,
    "закваска": 2,
}
