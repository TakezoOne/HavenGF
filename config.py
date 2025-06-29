import os

# 🔐 Авторизованные Telegram-пользователи (укажи свои ID)
AUTHORIZED_USERS = [
    123456789,  # ← замени на свой Telegram ID
    987654321
]

# 🔑 Ключи API из переменных окружения
TG_TOKEN = os.getenv("TG_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 📦 Пути к файлам хранения данных
DATA_FOLDER = "data"
DATA_FILE = os.path.join(DATA_FOLDER, "ingredients.json")
MINIMUMS_FILE = os.path.join(DATA_FOLDER, "minimums.json")
HISTORY_FILE = os.path.join(DATA_FOLDER, "history.json")
RECIPE_FILE = os.path.join(DATA_FOLDER, "recipe.json")

# 🛑 Минимальные остатки по умолчанию
DEFAULT_MINIMUMS = {
    "борошно": 5,
    "сіль": 1,
    "дріжджі": 0.5,
    "закваска": 0.5
}

