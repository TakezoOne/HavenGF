import re
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
from storage.storage import get_recipe, add_to_history
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def handle_production_phrase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()

    # 🔍 Проверка: фраза про виробництво білого хліба
    match = re.search(r'(сьогодні|сегодня)?\s*(\d+)\s+(білих|білий|хлібів)', user_text)
    if match:
        quantity = int(match.group(2))
        recipe_name = 'білий хліб'

        recipes = get_recipe()
        if recipe_name not in recipes:
            await update.message.reply_text("⚠️ Рецепт білого хліба не знайдено.")
            return

        single_recipe = recipes[recipe_name]
        full_ingredients = {
            ingredient: round(amount * quantity)
            for ingredient, amount in single_recipe.items()
        }

        # Відповідь
        lines = [f"🧮 Щоб зробити {quantity} {recipe_name} потрібно:"]
        for ingredient, total in full_ingredients.items():
            lines.append(f"• {ingredient}: {total} г")

        await update.message.reply_text("\n".join(lines))

        # Запис в історію
        add_to_history({
            "type": "виробництво",
            "recipe": recipe_name,
            "quantity": quantity,
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "ingredients_used": full_ingredients
        })
        return

    # 💬 Інакше — GPT-відповідь
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ти — розумний помічник пекаря. Відповідай українською мовою, коротко і по суті. Працюй тільки з виробничими питаннями."},
                {"role": "user", "content": user_text}
            ]
        )
        reply = response.choices[0].message.content.strip()
        if reply:
            await update.message.reply_text(reply)
        else:
            await update.message.reply_text("🤖 GPT не надав відповіді.")
    except Exception as e:
        print("GPT ERROR:", e)
        await update.message.reply_text("⚠️ Помилка при зверненні до GPT.")
