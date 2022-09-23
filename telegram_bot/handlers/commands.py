from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, CommandHandler
from telegram_bot.filter import filter
from database.db import exist_user, add_user, update_url


async def user_connect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    url = update.message.text
    msg = ''
    try:
        if exist_user(user_id):
            msg = update_url(user_id, url)
        else:
            msg = add_user(user_id, url)
    finally:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'{msg}'
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!"
    )


def list_handlers():
    start_handler = CommandHandler('start', start)
    url_handler = MessageHandler(filter.only_message, user_connect)
    return start_handler, url_handler
