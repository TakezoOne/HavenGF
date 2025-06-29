import os
import openai
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

from config import TG_TOKEN, OPENAI_API_KEY
from commands.returns import handle_return
from commands.need_to_buy import handle_need_to_buy
from commands.set_minimum import handle_set_minimum

# Устанавливаем ключ OpenAI
openai.api_key = "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"

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

# Обработка естественного текста (GPT)
async def gpt_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Ти — розумний помічник пекаря. Відповідай українською мовою, коротко і по суті. Працюй тільки з виробничими питаннями."
                },
                {"role": "user", "content": user_message}
            ]
        )
        reply = response['choices'][0]['message']['content']
        print("GPT ВІДПОВІДЬ:", reply)
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("⚠️ Помилка при зверненні до GPT.")
        print("GPT Error:", repr(e))

# Запуск фейкового сервера
threading.Thread(target=run_fake_web_server, daemon=True).start()

# Создание и настройка приложения
app = ApplicationBuilder().token(TG_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(handle_return)
app.add_handler(handle_need_to_buy)
app.add_handler(handle_set_minimum)
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), gpt_answer))

# Запуск бота
app.run_polling()
