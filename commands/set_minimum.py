from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from storage.storage import save_minimum
from config import ALLOWED_USERS

async def set_minimum_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("⛔ Недостатньо прав.")
        return

    try:
        name = context.args[0].lower()
        amount = float(context.args[1])
        save_minimum(name, amount)
        await update.message.reply_text(f"✅ Мінімум для '{name}' встановлено: {amount}")
    except:
        await update.message.reply_text("⚠️ Використання: /мінімум [назва] [кількість]")

handle_set_minimum = CommandHandler("minimum", set_minimum_command)
from telegram.ext import CommandHandler

handle_set_minimum = CommandHandler("minimum", set_minimum_command)
