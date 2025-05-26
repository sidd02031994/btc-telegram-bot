import os
import asyncio
from flask import Flask, request
import requests
from telethon import TelegramClient, events

# Load env variables
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# Flask setup
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ Bot is running!"

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    message = data.get("message", "⚠️ No message received from alert")
    send_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(send_url, data=payload)
    return {"status": "sent", "telegram_response": response.json()}

# Telethon setup
client = TelegramClient('anon', API_ID, API_HASH)

@client.on(events.Raw)
async def handler(event):
    if hasattr(event, 'reaction'):
        print("💬 Reaction detected:", event)

# Unified async entry point
async def start():
    await client.start(bot_token=BOT_TOKEN)
    print("✅ Telethon client started")

    # Run both Flask and Telethon
    await asyncio.gather(
        asyncio.to_thread(app.run, host="0.0.0.0", port=int(os.environ.get("PORT", 5000))),
        client.run_until_disconnected()
    )

if __name__ == "__main__":
    asyncio.run(start())
