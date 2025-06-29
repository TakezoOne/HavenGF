import os

# Токен Telegram и ключ OpenAI подгружаются из переменных окружения
TG_TOKEN = os.getenv("TG_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Список разрешённых пользователей (добавь свой Telegram ID)
ALLOWED_USERS = [
    5874151668,  # ← замени на свой настоящий Telegram ID
]

# Пути к файлам
DATA_FOLDER = "data"
INGREDIENTS_FILE = os.path.join(DATA_FOLDER, "ingredients.json")
MINIMUMS_FILE = os.path.join(DATA_FOLDER, "minimums.json")
HISTORY_FILE = os.path.join(DATA_FOLDER, "history.json")
RECIPE_FILE = os.path.join(DATA_FOLDER, "recipe.json")

# Минимальные остатки по умолчанию (можно изменить)
DEFAULT_MINIMUMS = {
    "борошно": 5,
    "сіль": 1,
    "вода": 10,
    "закваска": 2,
}
