from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def confirm_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Yes"), KeyboardButton(text="No")]
        ],
        resize_keyboard=True
    )
