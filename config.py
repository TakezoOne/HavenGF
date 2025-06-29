import os

# Токен Telegram и ключ OpenAI подгружаются из переменных окружения
TG_TOKEN = os.getenv("TG_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Список разрешённых пользователей (только они могут использовать бота)
ALLOWED_USERS = [
    123456789  # здесь позже вставим твой Telegram ID
]

# Пути к файлам с данными
DATA_FOLDER = "data"
INGREDIENTS_FILE = os.path.join(DATA_FOLDER, "ingredients.json")
MINIMUMS_FILE = os.path.join(DATA_FOLDER, "minimums.json")
HISTORY_FILE = os.path.join(DATA_FOLDER, "history.json")
RECIPE_FILE = os.path.join(DATA_FOLDER, "recipe.json")


