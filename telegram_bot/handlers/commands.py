from telegram_bot.config import config
from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, CommandHandler
from telegram_bot.filter import filter


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!"
    )
    await context.bot.send_message(
        chat_id=config.admin,
        text="Bot started to use +1 user"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text
    )


def list_handlers():
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filter.only_message, echo)
    return start_handler, echo_handler
