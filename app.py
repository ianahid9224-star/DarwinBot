import os
import requests
import telebot

# Токены из переменных окружения (Render -> Environment Variables)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Hugging Face endpoint (можно заменить на другую модель, например gpt2, mistralai/Mistral-7B-Instruct-v0.2 и др.)
API_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def ask_huggingface(text):
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        data = response.json()
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]
        elif isinstance(data, dict) and "error" in data:
            return "⚠️ Ошибка модели: " + data["error"]
        else:
            return "🤖 Не понял ответа от модели."
    except Exception as e:
        return "⚠️ Ошибка: " + str(e)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Привет 👋 Я твой ИИ-бот! Напиши что-нибудь.")

@bot.message_handler(func=lambda message: True)
def reply(message):
    user_input = message.text
    bot.send_chat_action(message.chat.id, "typing")
    answer = ask_huggingface(user_input)
    bot.send_message(message.chat.id, answer)

print("✅ Бот запущен!")
bot.infinity_polling()
