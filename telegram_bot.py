import os
import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from .utils import extract_aliexpress_url, is_valid_aliexpress_url
from .aliexpress_api import generate_affiliate_link

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Send me an AliExpress product link, and I will generate an affiliate link for you.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    original_url = extract_aliexpress_url(message_text)

    if original_url and is_valid_aliexpress_url(original_url):
        await update.message.reply_text('Processing your AliExpress link...') # Acknowledge
        affiliate_link = generate_affiliate_link(original_url) # This is a blocking call, consider async if needed

        if affiliate_link:
            response_text = f"Here is your affiliate link:\n{affiliate_link}"
             # Optional: Add product title/price if you fetch it
            await update.message.reply_text(response_text)
        else:
            await update.message.reply_text('Sorry, I could not generate an affiliate link for that URL. Please check the link or try again later.')
    elif "aliexpress.com" in message_text: # If it looks like AE but didn't match
         await update.message.reply_text("Please send a valid AliExpress product link (e.g., one starting with aliexpress.com/item/...).")
    # else: Ignore messages that don't contain AliExpress links


def create_telegram_application():
    if not BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set.")

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    # Handle text messages that are not commands
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    return application
