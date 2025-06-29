from telegram import Update
from telegram.ext import ContextTypes
from storage.storage import get_ingredients, get_minimums

async def what_to_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ingredients = get_ingredients()
    minimums = get_minimums()

    to_buy = []
    for name, min_amount in minimums.items():
        current = ingredients.get(name, 0)
        if current < min_amount:
            to_buy.append(f"{name}: {current} із мінімуму {min_amount}")

    if to_buy:
        message = "🔔 Потрібно купити:\n" + "\n".join(to_buy)
    else:
        message = "✅ Усі інгредієнти в нормі."

    await update.message.reply_text(message)
