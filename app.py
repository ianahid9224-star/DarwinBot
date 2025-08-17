import telebot
import os
from openai import OpenAI

# Берём ключи из переменных окружения Render
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

@bot.message_handler(func=lambda message: True)
def chat_with_ai(message):
    try:
        user_text = message.text

        # Отправляем текст в OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # можно gpt-4o или gpt-3.5-turbo
            messages=[{"role": "user", "content": user_text}],
            max_tokens=200
        )

        reply = response.choices[0].message.content
        bot.reply_to(message, reply)

    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

print("🤖 Бот запущен...")
bot.polling()
