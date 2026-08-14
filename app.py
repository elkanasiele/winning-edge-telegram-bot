import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================================================
# CONFIGURATION
# =========================================================

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError(
        "TELEGRAM_BOT_TOKEN is missing. "
        "Add TELEGRAM_BOT_TOKEN in Render Environment Variables."
    )

PORT = int(os.getenv("PORT", "10000"))

PAYMENT_LINK = "https://paystack.shop/pay/-ck9j9uxpa"


# =========================================================
# RENDER WEB SERVER
# =========================================================

app = Flask(__name__)


@app.route("/")
def home():
    return "Telegram bot is running successfully."


@app.route("/health")
def health():
    return "OK"


def run_web_server():
    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=False,
        use_reloader=False,
    )


# =========================================================
# TELEGRAM BOT COMMANDS
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    name = user.first_name if user and user.first_name else "there"

    message = (
        f"Hello {name}! 👋\n\n"
        "Welcome to Winning Edge Society.\n\n"
        "Use the buttons below by typing one of these commands:\n\n"
        "/subscribe - Subscription payment\n"
        "/payment - Payment instructions\n"
        "/help - Help"
    )

    await update.message.reply_text(message)


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "💳 *SUBSCRIPTION PAYMENT*\n\n"
        "Kindly complete your subscription payment using the secure "
        "Paystack payment link below:\n\n"
        f"{PAYMENT_LINK}\n\n"
        "After completing your payment, please send your payment "
        "confirmation to the administrator."
    )

    await update.message.reply_text(
        message,
        parse_mode="Markdown",
        disable_web_page_preview=False,
    )


async def payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "💳 *PAYMENT INSTRUCTIONS*\n\n"
        "1. Open the secure payment link below.\n"
        "2. Complete your subscription payment.\n"
        "3. Keep your payment confirmation.\n"
        "4. Send the confirmation to the administrator.\n\n"
        f"🔗 {PAYMENT_LINK}"
    )

    await update.message.reply_text(
        message,
        parse_mode="Markdown",
        disable_web_page_preview=False,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "🆘 *HELP*\n\n"
        "/start - Start the bot\n"
        "/subscribe - Make subscription payment\n"
        "/payment - View payment instructions\n"
        "/help - Show this help message"
    )

    await update.message.reply_text(
        message,
        parse_mode="Markdown",
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    text = update.message.text.lower().strip()

    if "payment" in text or "pay" in text or "subscribe" in text:
        await payment(update, context)
    elif "hello" in text or "hi" in text:
        await start(update, context)
    else:
        await update.message.reply_text(
            "Welcome to Winning Edge Society.\n\n"
            "Use /subscribe to make your subscription payment "
            "or /help to see available commands."
        )


# =========================================================
# MAIN
# =========================================================

def main():
    # Start Render's web server in the background
    web_thread = threading.Thread(
        target=run_web_server,
        daemon=True,
    )
    web_thread.start()

    # Create Telegram application
    telegram_app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    telegram_app.add_handler(
        CommandHandler("start", start)
    )

    telegram_app.add_handler(
        CommandHandler("subscribe", subscribe)
    )

    telegram_app.add_handler(
        CommandHandler("payment", payment)
    )

    telegram_app.add_handler(
        CommandHandler("help", help_command)
    )

    # Normal messages
    telegram_app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    print("Telegram bot is starting...")
    print(f"Render web server running on port {PORT}")

    # Start Telegram polling
    telegram_app.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
