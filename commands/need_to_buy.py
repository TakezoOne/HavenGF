from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from storage.storage import get_ingredients, get_minimums

async def need_to_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ingredients = get_ingredients()
    minimums = get_minimums()

    to_buy = []
    for name, min_amount in minimums.items():
        current = ingredients.get(name, 0)
        if current < min_amount:
            to_buy.append(f"{name}: {current} < {min_amount}")

    if to_buy:
        message = "🛒 Потрібно докупити:\n" + "\n".join(to_buy)
    else:
        message = "✅ Усі інгредієнти в достатній кількості."

    await update.message.reply_text(message)

handle_need_to_buy = CommandHandler("що_купити", need_to_buy)
