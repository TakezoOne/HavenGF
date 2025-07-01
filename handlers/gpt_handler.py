import re
import os
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
from storage.storage import get_recipe, add_to_history
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def handle_production_phrase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()
    recipes = get_recipe()

    # 🔍 Сформувати патерн з усіх назв рецептів
    pattern = r"(сьогодні|сегодня)?\s*(\d+)\s+(" + "|".join(recipes.keys()) + r")"
    match = re.search(pattern, user_text)

    if match:
        quantity = int(match.group(2))
        recipe_name = match.group(3)

        if recipe_name not in recipes:
            await update.message.reply_text(f"⚠️ Рецепт '{recipe_name}' не знайдено.")
            return

        single_recipe = recipes[recipe_name]
        full_ingredients = {
            ingredient: round(amount * quantity)
            for ingredient, amount in single_recipe.items()
        }

        lines = [f"🧮 Щоб зробити {quantity} {recipe_name} потрібно:"]
        for ingredient, total in full_ingredients.items():
            lines.append(f"• {ingredient}: {total} г")

        await update.message.reply_text("\n".join(lines))

        # 📝 Запис у історію
        add_to_history({
            "type": "виробництво",
            "recipe": recipe_name,
            "quantity": quantity,
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "ingredients_used": full_ingredients
        })
        return

    # 🧠 GPT-відповідь
    try:
        print("🔧 GPT ЗАПИТ:", user_text)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ти — розумний помічник пекаря. Відповідай українською, коротко і по суті. Працюй тільки з виробничими питаннями."},
                {"role": "user", "content": user_text}
            ]
        )
        reply = response.choices[0].message.content.strip()
        print("🔧 GPT ВІДПОВІДЬ:", reply)

        if reply:
            await update.message.reply_text(reply)
        else:
            await update.message.reply_text("🤖 GPT не надав відповіді.")
    except Exception as e:
        print("❌ GPT ERROR:", e)
        await update.message.reply_text("❌ Помилка GPT: " + str(e))
