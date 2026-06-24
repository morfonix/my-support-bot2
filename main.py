import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import google.generativeai as genai

# Получаем ключи из переменных окружения (которые ты настроил в Render)
TOKEN = os.environ.get("8815310236:AAG8kkGb1cqIgMW1OGBnMJyXrnV90Rq5iR8")
GEMINI_KEY = os.environ.get("AQ.Ab8RN6KeqUsEG44XoyCWaJCqx9VrxJevdwLfH1vqykAxR2rllw")

# Настройка ИИ
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

SYSTEM_PROMPT = """
Ты — эмпатичный и поддерживающий собеседник. Твоя задача — слушать пользователя, 
проявлять участие и помогать ему выразить свои чувства. 
ВАЖНО: Ты не врач. Если пользователь пишет о мыслях о причинении вреда себе или другим, 
обязательно посоветуй обратиться к профессиональному психологу.
"""

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет. Я здесь, чтобы выслушать тебя. О чем ты хочешь поговорить?")

@dp.message()
async def handle_message(message: types.Message):
    try:
        # Отправляем сообщение в ИИ
        response = model.generate_content(f"{SYSTEM_PROMPT}\nПользователь говорит: {message.text}")
        await message.answer(response.text)
    except Exception as e:
        logging.error(f"Ошибка API: {e}")
        await message.answer("Извини, я сейчас немного занят, попробуй написать чуть позже.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())