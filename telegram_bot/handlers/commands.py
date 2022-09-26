from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler
import gspread
from database.db import get_url_address, update_value, get_value
from telegram_bot.filter import filter
from google_sheets.authentication.auth import user_connect
from config import config


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Hello, {update.message.from_user.first_name}!"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Catch instruction!\n"
             f"Open https://docs.google.com/spreadsheets/d/1C-Z0OPYnyKPSjn8_YvrpE4uFIPiw0xQrSTn2OHhPVO4/edit#gid=1785411570"
             f"\nClick 'File'\n"
             f"Click 'Make a copy'\n"
             f"Click 'Share' and share access for editing with\n"
             f"`telegram-bot-service@counter-bot-361806.iam.gserviceaccount.com`\n"
             f"Copy URL of a page and send it to me!" # TODO use url here
    )


async def filter_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    line = 'https'
    msg = ''

    if update.message.text.__contains__(line):
        url = update.message.text
        msg_start = user_connect(user_id, url)
        msg = f'{msg_start}\n' \
              f'\nWrite a number & a category in the next message, please'

    elif get_url_address(user_id):
        url_wks = f'{get_url_address(user_id)}'
        gc = gspread.service_account()
        wks2 = gc.open_by_url(f'{url_wks}').sheet1


        def find_word():
            index = -1
            for item in config.keys:
                for i in item:
                    if update.message.text.lower().__contains__(i):
                        index = config.keys.index(item)
                        break
            if index == 0:    word_= 'Salary'
            elif index == 1:    word_ = 'Apartment'
            elif index == 2:    word_ = 'Mobile phone'
            elif index == 3:    word_ = 'Nutrition'
            elif index == 4:    word_ = 'Education'
            elif index == 5:    word_ = 'Health and hygiene'
            elif index == 6:    word_ = 'Transport'
            elif index == 7:    word_ = 'Clothing'
            elif index == 8:    word_ = 'Way of life (побут)'
            elif index == 9:    word_ = 'Travelling'
            else:    word_ = update.message.text.lower().capitalize()

            cell_ = wks2.find(f'{word_}')
            return True and cell_

        if update.message.text.isnumeric():
            user_id = update.message.from_user.id
            value = float(update.message.text)
            update_value(user_id, value)
            msg = 'Great! Write a category!'


        elif find_word():
            cell = find_word()
            new_value = get_value(user_id)
            before = wks2.cell(row=cell.row, col=(cell.col + 1)).value
            if not before:
                before = 0
            after = float(before) + new_value
            #print("Text found at R%sC%s" % (cell.row, cell.col))
            wks2.update_cell(row=cell.row, col=(cell.col + 1), value=after)

            msg = f'{new_value} was inserted to {update.message.text.capitalize()}'

        else:
            msg = 'Error occurred(\n' \
                  'Write a number & a category in the next message, please'
    else:
        msg = "Send your url, please"

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=msg
    )


def list_commands():
    start_handler = CommandHandler('start', start)
    filter_handlers = MessageHandler(filter.only_message, filter_handler)
    return start_handler, filter_handlers

# TODO command to see general expenses and limit of money (say to user that limit is 10% from income)
# TODO command to see a table from a picture (picture from a link)
# TODO middleware
