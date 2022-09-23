import gspread
from database.db import get_url_address
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler


async def do_sth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if get_url_address(user_id):
        url_wks = f'{get_url_address(user_id)}'
        gc = gspread.service_account()

        #wks = gc.open("expenses per month").sheet1
        wks2 = gc.open_by_url(f'{url_wks}').sheet1
        line = wks2.acell('G2').value

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'{line}'
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Send your url, please"
        )


def list_handlers_auth():
    do_handler = CommandHandler('do', do_sth)
    return do_handler

# TODO Check README.md
# TODO Uninstall a google-sheets library
# TODO check if the name of a sheet is equal to a month and create a new one if not!
