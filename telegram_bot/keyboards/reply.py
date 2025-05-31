from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from telegram_bot.handlers.manage_start import i18n


async def confirm_keyboard(user_id: int):
    yes = await i18n.get(key="messages.confirm.yes", user_id=user_id)
    no = await i18n.get(key="messages.confirm.no", user_id=user_id)

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=yes), KeyboardButton(text=no)]
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
        is_persistent=True
    )


async def category_actions_keyboard(user_id: int):
    add_btn_str = await i18n.get(key="buttons.add_cat", user_id=user_id)
    del_btn_str = await i18n.get(key="buttons.del_cat", user_id=user_id)
    cancel_btn_str = await i18n.get(key="buttons.cancel", user_id=user_id)

    return ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(text=add_btn_str),
            KeyboardButton(text=del_btn_str),
            KeyboardButton(text=cancel_btn_str)
        ]],
        resize_keyboard=True,
        one_time_keyboard=False,
        is_persistent=True
    )


async def cancel_button(user_id: int):
    cancel_btn_str = await i18n.get(key="buttons.cancel", user_id=user_id)

    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=cancel_btn_str)]],
        resize_keyboard=True,
        one_time_keyboard=False,
        is_persistent=True
    )


async def category_list_keyboard(categories):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=f'{cat}')] for cat in categories],
        resize_keyboard=True,
        one_time_keyboard=False,
        is_persistent=True
    )
