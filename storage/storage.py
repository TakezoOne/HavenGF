import json
import os
from datetime import datetime
from config import INGREDIENTS_FILE, MINIMUMS_FILE, HISTORY_FILE, RECIPE_FILE, DEFAULT_MINIMUMS

def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# --- Ингредиенты ---
def get_ingredients():
    return load_json(INGREDIENTS_FILE)

def save_ingredients(data):
    save_json(INGREDIENTS_FILE, data)

# --- Минимальные уровни ---
def get_minimums():
    data = load_json(MINIMUMS_FILE)
    return {**DEFAULT_MINIMUMS, **data}

def save_minimum(name, amount):
    data = load_json(MINIMUMS_FILE)
    data[name] = amount
    save_json(MINIMUMS_FILE, data)

# --- История действий ---
def add_to_history(entry):
    data = load_json(HISTORY_FILE)
    now = datetime.now().isoformat()
    data[now] = entry
    save_json(HISTORY_FILE, data)

def get_history():
    return load_json(HISTORY_FILE)

# --- Рецепт ---
def get_recipe():
    return load_json(RECIPE_FILE)
