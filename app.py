import requests
import telebot
import os

# === Настройки (замени токены на свои в Render) ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")   # токен от BotFather
HF_API_KEY = os.getenv("HF_API_KEY")           # токен от HuggingFace
HF_MODEL = os.getenv("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "Ты дружелюбный помощник. Отвечай понятно и по шагам.")
MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", "400"))

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode="HTML")

def hf_generate(user_text: str) -> str:
    url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    prompt = f"{SYSTEM_PROMPT}\n\nПользователь: {user_text}\nАссистент:"
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": MAX_NEW_TOKENS,
            "temperature": 0.7,
            "return_full_text": False
        }
    }
    r = requests.post(url, headers=headers, json=payload, timeout=120)
    data = r.json()
    if isinstance(data, list) and data and "generated_text" in data[0]:
        return data[0]["generated_text"].strip()
    return "⚠️ Ошибка ответа. Попробуй ещё раз."

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Привет! Я твой AI-бот 🤖 Напиши вопрос!")

@bot.message_handler(func=lambda m: True)
def reply(message):
    bot.send_chat_action(message.chat.id, "typing")
    answer = hf_generate(message.text)
    bot.reply_to(message, answer)

print("✅ Бот запущен!")
bot.infinity_polling()
