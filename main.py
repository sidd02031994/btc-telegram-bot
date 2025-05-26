
from flask import Flask, request
from telethon import TelegramClient, events
import threading
import requests
import os

# === Flask App to Handle Webhook Alerts from TradingView ===
app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

@app.route("/", methods=["GET"])
def home():
    return "✅ Bot is running!"

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    message = data.get("message", "⚠️ No message received from alert")

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=payload)

    return {"status": "sent", "telegram_response": response.json()}

# === Telethon Client to Track Reactions ===
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")

client = TelegramClient("session", API_ID, API_HASH)

active_users = set()

@client.on(events.Raw)
async def track_reactions(event):
    if hasattr(event, "reactions") or hasattr(event, "message"):
        try:
            if hasattr(event.message, "from_id") and hasattr(event.message, "reactions"):
                user_id = event.message.from_id.user_id
                active_users.add(user_id)
                print(f"✅ Reaction from user ID: {user_id}")
        except:
            pass

# === Start Both Flask + Telethon Using Threading ===
def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

def run_telethon():
    client.run_until_disconnected()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    threading.Thread(target=run_telethon).start()
