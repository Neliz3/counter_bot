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
from telegram_bot.dialogs.getters import get_email, get_trainings, get_cash_flow
from telegram_bot.dialogs.callbacks import (entered_email, trainings_type_factory, entered_training_text,
                                            callback_error, email_type_factory,
                                            cash_flow_type_factory, entered_cash_flow_text)
from telegram_bot.config import get_message
import asyncio


main_dialog = Dialog(
    Window(
        Const(asyncio.run(get_message("start.trainings"))),
        TextInput(
            id="trainings",
            type_factory=trainings_type_factory,
            on_error=callback_error,
            on_success=entered_training_text,
        ),
        state=SGMain.trainings,
        getter=get_trainings,
    ),
)


cash_flow_dialog = Dialog(
    Window(
        Const("↬"),
        TextInput(
            id="cash_flow",
            on_error=callback_error,
            on_success=entered_cash_flow_text,
            type_factory=cash_flow_type_factory,
        ),
        state=SGCashFlow.cash_flow,
        getter=get_cash_flow,
    ), # TODO: create logic to handle cash flow errors
    Window(
        # Const(asyncio.run(get_message("cash_flow.error"))),
        state=SGCashFlow.error_cash_flow,
        # Button, choose yes, no ...
    ),
)


email_dialog = Dialog(
    Window(
        Const(asyncio.run(get_message("email"))),
        TextInput(
            id="email",
            on_error=callback_error,
            on_success=entered_email,
            type_factory=email_type_factory,
        ),
        state=SGEmail.email,
        getter=get_email,
    )
)
