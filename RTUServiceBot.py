from typing import Final
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import logging
import os

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# Get bot token from environment
TOKEN: Final = os.getenv("BOT_TOKEN")
BOT_USERNAME: Final = '@RTUService_bot'  # Optional, for mention tracking

# ─────────────────────────────────────────────────────────────
# Commands

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! Thanks for chatting with me! I'm RTUServiceBot, your assistant for RTU services."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🆘 *Help Menu*\n"
        "/start - Start talking to the bot\n"
        "/help - Show this help message\n"
        "/customer - Get customer service info for RTUServiceBot"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def customer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 RTUServiceBot Customer Service:\n"
        "Email: support@rtuservicebot.com\n"
        "Phone: +855 123 456 789"
    )

# ─────────────────────────────────────────────────────────────
# Text handler

def simple_response(text: str) -> str:
    processed = text.lower()
    if 'hello' in processed:
        return 'Hey there!'
    if 'how are you' in processed:
        return 'I am good!'
    if 'rtu' in processed:
        return 'RTU stands for Remote Terminal Unit, a device used in industrial control systems.'
    if 'service' in processed:
        return 'RTUServiceBot provides support for your RTU-related needs.'
    if 'i love python' in processed:
        return 'Remember to subscribe!'
    if 'coding' in processed or 'programming' in processed:
        return 'Coding is fun! Keep practicing every day.'
    return 'I do not understand what you wrote...'

# ─────────────────────────────────────────────────────────────
# Message handler

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text
    user_id = update.message.chat.id
    
    logging.info(f'User ({user_id}) in {message_type}: "{text}"')

    response = simple_response(text)
    logging.info('Bot response: %s', response)
    await update.message.reply_text(response)

# ─────────────────────────────────────────────────────────────
# Error handler

async def error(update: object, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Update {update} caused error: {context.error}", exc_info=True)

# ─────────────────────────────────────────────────────────────
# Main runner

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('customer', customer_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error)

    logging.info("🤖 RTUServiceBot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
