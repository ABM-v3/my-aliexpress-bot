import os
import asyncio
from flask import Flask, request, Response
import telegram
from telegram import Update
from telegram_bot import create_telegram_application # Import from your bot file

app = Flask(__name__)
application = create_telegram_application() # Initialize PTB application

# Define the webhook route Vercel will call
@app.route('/webhook', methods=['POST'])
async def webhook():
    if request.is_json:
        update_data = request.get_json()
        update = Update.de_json(update_data, application.bot)
        # Process the update using python-telegram-bot's dispatcher
        # Make sure your PTB setup correctly handles updates passed this way
        # Running process_update in the background is often recommended for webhooks
        # to avoid blocking the response to Telegram.
        asyncio.create_task(application.process_update(update))
        return Response(status=200) # Respond quickly to Telegram
    else:
        return Response("Bad Request", status=400)

# Optional: Route to set the webhook (run once manually or via a script)
@app.route('/set_webhook', methods=['GET'])
async def set_webhook():
    # Vercel provides the deployment URL via an environment variable
    # Default is VERCEL_URL, but might be VERCEL_BRANCH_URL etc. Check Vercel docs.
    # Ensure the URL starts with https://
    webhook_base_url = os.environ.get('VERCEL_URL')
    if not webhook_base_url:
         return "Error: VERCEL_URL not set. Cannot determine webhook URL."

    # Ensure it's https
    if not webhook_base_url.startswith("https://"):
         webhook_base_url = f"https://{webhook_base_url}"

    webhook_url = f"{webhook_base_url}/webhook" # Your webhook route

    await application.bot.set_webhook(webhook_url)
    return f"Webhook set to {webhook_url}"

# Optional: A root endpoint for health checks or info
@app.route('/')
def index():
    return "AliExpress Affiliate Bot is running!"

# Vercel runs the file, so Flask's built-in server isn't used directly in production
# The `app` object is used by Vercel's Python WSGI handler.
