import os
import openai
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from config import TG_TOKEN, OPENAI_API_KEY
from commands.returns import handle_return
from commands.need_to_buy import handle_need_to_buy
from commands.set_minimum import handle_set_minimum  # 👈 новая команда

openai.api_key = OPENAI_API_KEY

# === Фейковый веб-сервер, чтобы Render не ругался ===
class PingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_fake_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("", port), PingHandler)
    server.serve_forever()

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я бот-помічник пекарні. Напиши /help або просто задай питання.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/повернення [назва] [кількість] — запис повернення продукції\n"
        "/що_купити — список інгредієнтів, яких не вистачає\n"
        "/мінімум [назва] [кількість] — встановити мінімум\n"
        "Або просто пиши питання природною мовою!"
    )

# GPT-відповіді
async def gpt_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ти — розумний помічник пекаря. Відповідай українською мовою, коротко і по суті. Працюй тільки з виробничими питаннями."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response['choices'][0]['message']['content']
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("Помилка при зверненні до GPT.")
        print("GPT Error:", e)

# Запуск
threading.Thread(target=run_fake_web_server, daemon=True).start()

app = ApplicationBuilder().token(TG_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(handle_return)
app.add_handler(handle_need_to_buy)
app.add_handler(handle_set_minimum)  # 👈 добавили сюда
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), gpt_answer))
app.run_polling()
