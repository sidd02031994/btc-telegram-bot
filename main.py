import os
import logging
import asyncio
from flask import Flask, request
import requests
from threading import Thread
from telethon import TelegramClient, events

# === Flask App ===
app = Flask(__name__)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

@app.route("/", methods=["GET"])
def home():
    return "✅ Bot is running!"

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    message = data.get("message", "⚠️ No message received from alert")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, data=payload)

    return {"status": "sent", "telegram_response": response.json()}


# === Telethon Emoji Reaction Tracker ===
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = "reaction_tracker"

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.Raw)
async def reaction_logger(event):
    if hasattr(event, 'reactions'):
        print("🔁 Reaction Event Detected")
        print(event.stringify())

# === Run Telethon in background thread ===
def start_telethon():
    with client:
        print("🚀 Telethon bot running...")
        client.run_until_disconnected()

# === Start Both Flask and Telethon ===
if __name__ == "__main__":
    Thread(target=start_telethon).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
