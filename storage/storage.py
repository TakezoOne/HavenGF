import re
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
from storage.storage import get_recipe, add_to_history
from config import HISTORY_FILE

async def handle_production_phrase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()

    match = re.search(r'(\\d+)\\s+(білих|білий|білих хлібів)', user_text)
    if not match:
        return  # Не фраза про виробництво

    quantity = int(match.group(1))
    recipe_name = 'білий хліб'

    recipes = get_recipe()
    if recipe_name not in recipes:
        await update.message.reply_text("⚠️ Рецепт білого хліба не знайдено.")
        return

    single_recipe = recipes[recipe_name]
    full_ingredients = {}

    for ingredient, amount in single_recipe.items():
        total = round(amount * quantity)
        full_ingredients[ingredient] = total

    # Форматування відповіді
    lines = [f"Щоб зробити {quantity} {recipe_name} потрібно:"]
    for ingredient, total in full_ingredients.items():
        lines.append(f"• {ingredient}: {total} г")

    await update.message.reply_text("\\n".join(lines))

    # Запис у історію
    add_to_history({
        "type": "виробництво",
        "recipe": recipe_name,
        "quantity": quantity,
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "ingredients_used": full_ingredients
    })
