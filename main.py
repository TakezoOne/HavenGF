import json
import os
import openai
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Получаем токены из переменных окружения
TG_TOKEN = os.environ.get("TG_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

DATA_FILE = "ingredients.json"

# Загрузка/сохранение данных
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот-помощник пекарни. Напиши /help или задай вопрос.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/add_ingredient [название] [кол-во]\n"
        "/use_ingredient [название] [кол-во]\n"
        "/show_ingredients — остатки\n"
        "Можно просто писать вопросы, и я помогу как GPT."
    )

async def add_ingredient(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    try:
        name = context.args[0].lower()
        amount = float(context.args[1])
        data[name] = data.get(name, 0) + amount
        save_data(data)
        await update.message.reply_text(f"Добавлено {amount} {name}.")
    except:
        await update.message.reply_text("Пример: /add_ingredient мука 10")

async def use_ingredient(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    try:
        name = context.args[0].lower()
        amount = float(context.args[1])
        if name in data:
            data[name] = max(0, data[name] - amount)
            save_data(data)
            await update.message.reply_text(f"Использовано {amount} {name}. Осталось: {data[name]}")
        else:
            await update.message.reply_text(f"Ингредиент '{name}' не найден.")
    except:
        await update.message.reply_text("Пример: /use_ingredient мука 5")

async def show_ingredients(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    if not data:
        await update.message.reply_text("Ингредиенты не добавлены.")
    else:
        message = "\n".join([f"{k}: {v}" for k, v in data.items()])
        await update.message.reply_text("Остатки:\n" + message)

# GPT-обработка текста
async def gpt_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — помощник пекаря. Отвечай кратко, понятно и по делу."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response['choices'][0]['message']['content']
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("Ошибка при обращении к GPT.")
        print("GPT Error:", e)

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

# 🔃 Сначала запускаем фейковый сервер
threading.Thread(target=run_fake_web_server, daemon=True).start()

# 🔃 Затем запускаем Telegram-бота
app = ApplicationBuilder().token(TG_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("add_ingredient", add_ingredient))
app.add_handler(CommandHandler("use_ingredient", use_ingredient))
app.add_handler(CommandHandler("show_ingredients", show_ingredients))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), gpt_answer))
app.run_polling()
