
from flask import Flask, request
import requests
import os
import threading
from telethon import TelegramClient, events

app = Flask(__name__)

# Environment Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

# Validation
if not BOT_TOKEN or not CHAT_ID or not API_ID or not API_HASH:
    raise EnvironmentError("❌ One or more required environment variables are missing.")

API_ID = int(API_ID)

# TelegramClient setup
client = TelegramClient("reaction_tracker", API_ID, API_HASH)

# Flask Routes
@app.route("/", methods=["GET"])
def home():
    return "✅ BTC Breakout Bot is running!"

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    message = data.get("message", "⚠️ No message received from alert")

    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(telegram_url, data=payload)
    return {"status": "sent", "telegram_response": response.json()}

# Telethon background task
@client.on(events.Raw)
async def handler(event):
    if hasattr(event, "message_id") and hasattr(event, "peer"):
        print(f"📥 Reaction or event detected: {event}")

def start_telethon():
    try:
        with client:
            print("🚀 Telethon bot running...")
            client.run_until_disconnected()
    except Exception as e:
        print(f"❌ Telethon failed: {e}")

# Start Flask and Telethon
if __name__ == "__main__":
    telethon_thread = threading.Thread(target=start_telethon)
    telethon_thread.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
