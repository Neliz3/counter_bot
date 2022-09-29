from telegram import ReplyKeyboardMarkup, KeyboardButton


button_link = KeyboardButton('open table')
keyboard_reply = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False,
                                     keyboard=[[button_link]])
