import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
PAYSTACK_LINK = "https://paystack.shop/pay/-ck9j9uxpa"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("💳 PAY NOW", url=PAYSTACK_LINK)
    )
    keyboard.add(
        InlineKeyboardButton("✅ I HAVE PAID", callback_data="paid")
    )

    bot.send_message(
        message.chat.id,
        "🏆 *WINNING EDGE SOCIETY*\n\n"
        "Welcome!\n\n"
        "💳 Complete your subscription payment using the secure Paystack link below.\n\n"
        "After making payment, tap *I HAVE PAID*.",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

@bot.callback_query_handler(func=lambda call: call.data == "paid")
def paid(call):
    bot.answer_callback_query(call.id)
    bot.send_message(
        call.message.chat.id,
        "⏳ Your payment is being verified. Please wait for confirmation."
    )

print("Bot is running...")
bot.infinity_polling()
