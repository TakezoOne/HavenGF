import re
import os
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
from storage.storage import get_recipe, add_to_history
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🔁 Словник синонімів → нормалізуємо назви до імен з recipe.json
RECIPE_ALIASES = {
    "хліб": "білий хліб",
    "хлібів": "білий хліб",
    "білих": "білий хліб",
    "білий": "білий хліб",
    "фокач": "фокача",
    "фокачі": "фокача",
    "фокача": "фокача"
}

async def handle_production_phrase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()
    recipes = get_recipe()

    # 🔍 Шукаємо кількість і слово, яке може бути рецептом
    match = re.search(r"(сьогодні|сегодня)?\s*(\d+)\s+(\w+)", user_text)
    if match:
        quantity = int(match.group(2))
        raw_name = match.group(3)

        # 🎯 Нормалізація слова до назви рецепту
        recipe_name = RECIPE_ALIASES.get(raw_name)

        if recipe_name and recipe_name in recipes:
            single_recipe = recipes[recipe_name]
            full_ingredients = {
                ingredient: round(amount * quantity)
                for ingredient, amount in single_recipe.items()
            }

            lines = [f"🧮 Щоб зробити {quantity} {recipe_name} потрібно:"]
            for ingredient, total in full_ingredients.items():
                lines.append(f"• {ingredient}: {total} г")

            await update.message.reply_text("\n".join(lines))

            # 📝 Запис в історію
            add_to_history({
                "type": "виробництво",
                "recipe": recipe_name,
                "quantity": quantity,
                "datetime": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "ingredients_used": full_ingredients
            })
            return

    # 🧠 Якщо не знайдено — GPT
    try:
        print("🔧 GPT ЗАПИТ:", user_text)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
