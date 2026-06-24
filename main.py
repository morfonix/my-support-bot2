import logging
import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram import types
import google.generativeai as genai
from aiohttp import web

# Получаем данные
TOKEN = os.environ.get("8815310236:AAG8kkGb1cqIgMW1OGBnMJyXrnV90Rq5iR8")
GEMINI_KEY = os.environ.get("AQ.Ab8RN6KeqUsEG44XoyCWaJCqx9VrxJevdwLfH1vqykAxR2rllw")
PORT = int(os.environ.get("PORT", 10000))

# Настройка ИИ
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

# --- WEB-СЕРВЕР ДЛЯ RENDER ---
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    logging.info(f"Web server started on port {PORT}")

# --- ЛОГИКА БОТА ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет. Я здесь, чтобы выслушать тебя.")

@dp.message()
async def handle_message(message: types.Message):
    try:
        response = model.generate_content(f"Ты эмпатичный слушатель. Пользователь говорит: {message.text}")
        await message.answer(response.text)
    except Exception as e:
        logging.error(f"Ошибка API: {e}")

async def main():
    # Запускаем и сервер (чтобы Render был доволен), и бота
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())