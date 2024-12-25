from aiogram_dialog import Window
from telegram_bot.dialogs.states import SGEmail, SGMain, SGFlow
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const
from telegram_bot.dialogs.getters import get_email
from telegram_bot.dialogs.utils import error, email_type_factory, entered_email


# async def main_window():
#     return Window(
#         Const("Enter your email address:"),
#         TextInput(
#             id="email",
#             on_error=error,
#             on_success=entered_email,
#             type_factory=email_type_factory,
#         ),
#         state=SGEmail.email,
#         getter=get_email,
#     )


async def email_window():
    return Window(
        Const("Enter your email address:"),
        TextInput(
            id="email",
            on_error=error,
            on_success=entered_email,
            type_factory=email_type_factory,
        ),
        state=SGEmail.email,
        getter=get_email,
    )
