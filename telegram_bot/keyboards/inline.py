from telegram import InlineKeyboardButton, InlineKeyboardMarkup


keyboard = [[InlineKeyboardButton("See more details ☟", callback_data="details")]]

reply_markup = InlineKeyboardMarkup(keyboard)
