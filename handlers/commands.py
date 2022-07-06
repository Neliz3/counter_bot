from config import application, admin
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!"
    )
    await context.bot.send_message(
        chat_id=admin,
        text="Bot started to use +1 user"
    )


def list_handlers():
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
