from config import admin
from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, CommandHandler
from filter.filter import only_message


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!"
    )
    await context.bot.send_message(
        chat_id=admin,
        text="Bot started to use +1 user"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text
    )


def list_handlers():
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(only_message, echo)
    return start_handler, echo_handler
