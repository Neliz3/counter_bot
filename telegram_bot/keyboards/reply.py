from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def confirm_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Yes"), KeyboardButton(text="No")]
        ],
        resize_keyboard=True,
        one_time_keyboard = True
    )


def category_actions_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="➕ Add"), KeyboardButton(text="🗑 Delete")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def category_list_keyboard(categories):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=f'{cat}')] for cat in categories],
        resize_keyboard=True
    )
