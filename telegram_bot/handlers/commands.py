from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CommandHandler, MessageHandler
import gspread
from database.db import update_value, get_value, get_sheet_id
from telegram_bot.filter import filter
from telegram_bot.authentication.auth import user_connect
from config import config
from telegram_bot.keyboards.reply import keyboard_reply
from google_sheets.auth import share_access
from google_sheets.commands import get_pocket_value, set_pocket_value

# Giving instructions how to use an app
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_connect(user_id)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Hello, {update.message.from_user.first_name} ;)"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Write a number & a category in the next message, please"
    )


# # It operates all entered messages from a user and distributes them
# async def filter_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text = update.message.text
#     user_id = update.message.from_user.id
#
#     gc = gspread.service_account()
#     wks2 = gc.open_by_url(f'{url_wks}').sheet1
#
#     def find_word():
#         index = -1
#         for item in config.keys:
#             for i in item:
#                 if update.message.text.lower().__contains__(i):
#                     index = config.keys.index(item)
#                     break
#         if index == 0:  word_ = 'Salary'
#         elif index == 1:    word_ = 'Apartment'
#         elif index == 2:    word_ = 'Mobile phone'
#         elif index == 3:    word_ = 'Nutrition'
#         elif index == 4:    word_ = 'Education'
#         elif index == 5:    word_ = 'Health and hygiene'
#         elif index == 6:    word_ = 'Transport'
#         elif index == 7:    word_ = 'Clothing'
#         elif index == 8:    word_ = 'Way of life (побут)'
#         elif index == 9:    word_ = 'Travelling'
#         else:    word_ = update.message.text.lower().capitalize()
#
#         cell_ = wks2.find(f'{word_}')
#         return True and cell_
#
#     if update.message.text.isnumeric():
#         user_id = update.message.from_user.id
#         value = float(update.message.text)
#         update_value(user_id, value)
#         msg = 'Great! Write a category!'
#
#     elif find_word():
#         cell = find_word()
#
#         new_value = get_value(user_id)
#         before = wks2.cell(row=cell.row, col=(cell.col + 1)).value
#         if not before:
#             before = 0
#         after = float(before) + new_value
#         wks2.update_cell(row=cell.row, col=(cell.col + 1), value=after)
#
#         g_find = wks2.find('General expenses')
#         p_find = wks2.find('Pocket money')
#         data_g = wks2.cell(row=g_find.row, col=g_find.col + 1).value
#         data_p = wks2.cell(row=p_find.row, col=p_find.col + 1).value
#         add_msg = f'{data_p} grn | Pocket money\n' \
#                   f'-{data_g} grn | Costs'
#         if cell.col == 1:
#             msg = f'💱 {new_value} to {update.message.text.capitalize()}'
#         else:
#             msg = f'🛍️ -{new_value} to {update.message.text.capitalize()}'
#
#     else:
#         msg = 'Error occurred(\n' \
#               'Write a number & a category in the next message, please'
# else:
# msg = "Send your url, please"
#
# await context.bot.send_message(
#     chat_id=update.effective_chat.id,
#     text=msg
# )
# await context.bot.send_message(
#     chat_id=update.effective_chat.id,
#     text=add_msg
# )
#
#
# # Getting a value from a selected field
# async def get_expenses(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_id = update.message.from_user.id
#
#     if get_url_address(user_id):
#         url_wks = f'{get_url_address(user_id)}'
#         gc = gspread.service_account()
#         wks2 = gc.open_by_url(f'{url_wks}').sheet1
#         cell_ = wks2.find('General expenses')
#         data = wks2.cell(row=cell_.row, col=cell_.col + 1).value
#         msg = f'-{data} grn | Costs'
#     else:
#         msg = "Send your url, please"
#
#     await context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         text=f'{msg}'
#     )
#
#
# # Getting a value from a selected field
# async def get_pocket(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_id = update.message.from_user.id
#
#     if get_url_address(user_id):
#         url_wks = f'{get_url_address(user_id)}'
#         gc = gspread.service_account()
#         wks2 = gc.open_by_url(f'{url_wks}').sheet1
#         cell_ = wks2.find('Pocket money')
#         data = wks2.cell(row=cell_.row, col=cell_.col + 1).value
#         msg = f'{data} grn | Pocket money\n'
#     else:
#         msg = "Send your url, please"
#
#     await context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         text=f'{msg}'
#     )



async def get_pocket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    sheet_id = get_sheet_id(user_id)
    response_msg = set_pocket_value(sheet_id, 10500)
    pocket_value = get_pocket_value(sheet_id)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'{response_msg} Pocket value is: {pocket_value}'
    )


# Getting a gmail
async def give_sheet_for_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_email = "eliza.nadrega14@gmail.com" # TODO: get email from msg
    user_id = update.message.from_user.id

    sheet_id = get_sheet_id(user_id)
    response_msg = share_access(user_email, sheet_id)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=response_msg,
    )

def list_commands():
    start_handler = CommandHandler('start', start)
    # expenses_handler = CommandHandler('expenses', get_expenses)
    # pocket_handler = CommandHandler('pocket', get_pocket)
    # filter_handlers = MessageHandler(filter.only_message, filter_handler)
    get_sheet = CommandHandler('sheet', give_sheet_for_user)
    get_pocket_command = CommandHandler('pocket', get_pocket)
    return start_handler, get_sheet, get_pocket_command
