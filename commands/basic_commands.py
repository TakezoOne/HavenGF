from telegram import Update
from telegram.ext import ContextTypes
from storage.storage import get_ingredients, get_minimums
from config import ALLOWED_USERS

def is_authorized(user_id: int) -> bool:
    return user_id in ALLOWED_USERS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return await update.message.reply_text("⛔ Доступ заборонено.")
    await update.message.reply_text("Привіт! Я бот-помічник пекарні. Напиши /help або питання.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return await update.message.reply_text("⛔ Доступ заборонено.")
    await update.message.reply_text(
        "📋 Доступні команди:\n"
        "/start — запуск\n"
        "/help — допомога\n"
        "/залишки — показати залишки інгредієнтів\n"
        "/мінімальні — показати мінімальні рівні"
    )

async def show_ingredients(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return await update.message.reply_text("⛔ Доступ заборонено.")
    data = get_ingredients()
    if not data:
        await update.message.reply_text("Немає доданих інгредієнтів.")
    else:
        lines = [f"{name}: {amount}" for name, amount in data.items()]
        await update.message.reply_text("📦 Залишки:\n" + "\n".join(lines))

async def show_minimums(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return await update.message.reply_text("⛔ Доступ заборонено.")
    data = get_minimums()
    lines = [f"{name}: {amount}" for name, amount in data.items()]
    await update.message.reply_text("📉 Мінімальні рівні:\n" + "\n".join(lines))
