from flask import Flask, request
import requests
import os

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))