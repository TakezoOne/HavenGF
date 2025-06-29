import os

# Авторизованные пользователи (ID телеграм-юзеров)
AUTHORIZED_USERS = [123456789, 987654321]  # ← замени на свои ID

# Ключи из Render переменных окружения
TG_TOKEN = os.getenv("TG_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Минимальные остатки по умолчанию (если не заданы)
DEFAULT_MINIMUMS = {
    "борошно": 5,
    "сіль": 1,
    "дріжджі": 0.5,
    "закваска": 0.5
}
