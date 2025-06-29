from telegram import Update
from telegram.ext import ContextTypes
from storage.storage import add_to_history
from config import ALLOWED_USERS

async def handle_return(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("⛔ У вас немає доступу до бота.")
        return

    try:
        name = context.args[0].lower()
        amount = float(context.args[1])
    except (IndexError, ValueError):
        await update.message.reply_text("⚠️ Приклад: /повернення хліб 3")
        return

    add_to_history({
        "type": "повернення",
        "назва": name,
        "кількість": amount,
        "від": user_id
    })
    await update.message.reply_text(f"✅ Повернення зафіксовано: {amount} × {name}")
