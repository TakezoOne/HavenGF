import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from openai import OpenAI

# 🔐 Получаем ключи из переменных окружения (Render)
TG_TOKEN = os.getenv("TG_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_KEY)

# 📂 Импорт команд
from commands.returns import handle_return
from commands.need_to_buy import handle_need_to_buy
from commands.set_minimum import handle_set_minimum

# 📂 Главный обработчик — считает рецепты и отвечает GPT
from handlers.gpt_handler import handle_production_phrase

# === Фейковый веб-сервер для Render ===
class PingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_fake_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("", port), PingHandler)
    server.serve_forever()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я бот-помічник пекарні. Напиши /help або просто задай питання.")

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/повернення [назва] [кількість] — запис повернення продукції\n"
        "/shcho_kupyty — список інгредієнтів, яких не вистачає\n"
        "/minimum [назва] [кількість] — встановити мінімум для інгредієнта\n"
        "Або просто пиши питання природною мовою!"
    )

# 🔄 Запуск фейкового веб-сервера (для Render)
threading.Thread(target=run_fake_web_server, daemon=True).start()

# ▶️ Запуск Telegram-бота
app = ApplicationBuilder().token(TG_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(handle_return)
app.add_handler(handle_need_to_buy)
app.add_handler(handle_set_minimum)
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_production_phrase))  # универсальный обработчик
app.run_polling()
