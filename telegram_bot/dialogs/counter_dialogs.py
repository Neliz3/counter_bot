from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Cancel,
    Column,
    Next,
    Row,
    ScrollingGroup,
    Select,
    Start,
)
from aiogram_dialog.widgets.text import Const, Format, Multi
from telegram_bot.dialogs.states import SGEmail, SGMain, SGCashFlow
from telegram_bot.dialogs.getters import get_email, get_start_train, get_cash_flow
from telegram_bot.dialogs.utils import error, email_type_factory
from telegram_bot.dialogs.callbacks import entered_email, check_user_input, entered_train_text, invalid_train_text
from telegram_bot.config import get_message
import asyncio

setup_dialog = Dialog(
    Window(
        Const(asyncio.run(get_message("start.example"))),
        TextInput(
            id="start_train",
            filter=check_user_input,
            
        )
        state=SGMain.start_train,
        getter=get_start_train,
)
)

# async def email_window():
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
