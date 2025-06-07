import os
import asyncio
import threading
from flask import Flask, request
import requests
from telethon import TelegramClient, events, Button

app = Flask(__name__)

# Environment Variables for breakout bot\BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID   = os.getenv("CHAT_ID")
API_ID    = os.getenv("API_ID")
API_HASH  = os.getenv("API_HASH")

# Validation
if not BOT_TOKEN or not CHAT_ID or not API_ID or not API_HASH:
    raise EnvironmentError("❌ One or more required environment variables are missing.")

# Convert API_ID to int
API_ID = int(API_ID)

# --- TelegramClient setup ---
client = TelegramClient('anon', API_ID, API_HASH)

# --- Flask Routes for breakout alerts ---
@app.route("/", methods=["GET"])
def home():
    return "✅ BTC Breakout Bot is running!"

@app.route("/", methods=["POST"])
def webhook():
    data = request.json or {}
    message = data.get("message", "⚠️ No message received from alert")

    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(telegram_url, data=payload)
    return {"status": "sent", "telegram_response": response.json()}

# --- Telethon event for breakout reactions/logging ---
@client.on(events.Raw)
async def handler(event):
    if hasattr(event, "message_id") and hasattr(event, "peer"):
        print(f"📥 Reaction or event detected: {event}")

# --- Telethon event: greet new members with buttons ---
@client.on(events.ChatAction)
async def greet_new_members(event):
    # Only act on member joins or adds
    if not (event.user_joined or event.user_added):
        return

    for user_id in event.action_message.users:
        user = await client.get_entity(user_id)
        name = user.first_name or user.username or "there"
        # Build rich welcome message
        text = (
            "👋 *Welcome to the Channel!*\n\n"
            "Thank you for joining our trading community. Here’s everything you need to jumpstart both your traditional and crypto trading journey:\n\n"
            "📚 *Free Trading Resources*\n"
            "Get instant access to our hand-picked toolkit for traders at every level:"
        )

        # Buttons for free resources
        buttons = [
            [Button.url("📚 Free Resources", "https://spf.bio/TrDKe")]
        ]

        # Continue message
        text += (
            "\n\n💎 *Exclusive Crypto Perks on Delta Exchange*\n"
            "Open your account with my link and unlock:\n"
            "• Free access to my comprehensive Crypto Trading Course\n"
            "• Entry into our Premium Community for live Q&A, trade ideas, and networking\n"
            "• Pro updates to the Liquidity Trap Indicator—never miss a high-probability setup\n\n"
            "Getting started is easy:"            
        )

        # Button for Delta signup
        buttons.append([
            Button.url("🚀 Sign up on Delta Exchange", "https://spf.bio/7yWGI")
        ])

        # Final instructions appended
        text += (
            "\n1. Complete the KYC process\n"
            "2. Send a screenshot of your approved KYC at `hi@siddhantkesiddhant.com` to claim your bonuses\n\n"
            "Have questions? Drop them anytime—our community and I are here to help you trade smarter. Let’s make those winning trades! 🚀"
        )

        # Send with markdown and inline buttons
        await client.send_message(
            event.chat_id,
            text,
            buttons=buttons,
            parse_mode="markdown"
        )

# --- Start both Flask and Telethon ---
def start_telethon():
    with client:
        print("🚀 Telethon bot running with both breakout & greet handlers...")
        client.run_until_disconnected()

if __name__ == "__main__":
    # Start Telethon in a background thread
    telethon_thread = threading.Thread(target=start_telethon, daemon=True)
    telethon_thread.start()

    # Start Flask server for breakout webhook
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
