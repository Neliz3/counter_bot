import asyncio
from google_sheets.commands import update_value
from aiogram.types import Message
from database.db import database as db, Database
from google_sheets.auth import share_access_sync
from aiogram_dialog import DialogManager, StartMode, ShowMode
from typing import Any
from aiogram_dialog.widgets.input import ManagedTextInput
from telegram_bot.dialogs.states import SGCashFlow, SGMain, SGEmail, SGSetup
from telegram_bot.config import get_message
from config.config import categories
import re

from telegram_bot.keyboards.reply import cash_flow_hint


async def entered_training_text(
        message: Message,
        widget: ManagedTextInput[str],
        dialog_manager: DialogManager,
        value: str,
):
    congratulations = await get_message("start.trainings_end")
    cash_flow_help = await get_message("cash_flow.help")
    await message.answer(congratulations)
    await message.answer(cash_flow_help)

    await dialog_manager.start(SGCashFlow.cash_flow,
                                   mode=StartMode.RESET_STACK)


# Custom user input train validation function for type_factory
def trainings_type_factory(value: str) -> str:
    input_correct = "300 taxi"
    if input_correct == value:
        return value
    raise ValueError()


# User input cash flow validation
def cash_flow_type_factory(value: str) -> str:
    cash_flow_pattern = r"^\d+\s+[a-zA-Z ]+$"
    if re.match(cash_flow_pattern, value):
        return value
    raise ValueError()


async def entered_cash_flow_text(
        message: Message,
        widget: ManagedTextInput[str],
        dialog_manager: DialogManager,
        text: str,
):
    # TODO: fix the same error NOT FOUND CAT on different parts
    items = text.split()
    # Get value from msg
    value = items[0]

    # Get category from msg
    cat = " ".join(items[1:])

    # Search & validate the exact category
    # TODO: make categories synonyms using GPT
    for keys, cats in categories.items():
        if cat in cats:
            cat = cats[0]
            break
    else:
        await dialog_manager.switch_to(SGCashFlow.error_cash_flow)

    # Save to sheets
    user_id = message.from_user.id
    spreadsheet_id = await Database().get_spreadsheet_id(db, user_id)
    try:
        await update_value(spreadsheet_id, cat, value)
    except ValueError:
        await dialog_manager.switch_to(SGCashFlow.error_cash_flow)
    else:
        result = await get_message("cash_flow.result",
                                   value=value, cat=cat)
        await message.answer(result)


async def callback_error(
        message: Message,
        dialog_: Any,
        manager: DialogManager,
        error_: ValueError
):
    error_msg = await get_message("error")
    await message.answer(error_msg)


# Custom email validation function for type_factory
def email_type_factory(value: str) -> str:
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    if re.match(email_regex, value):
        return value
    raise ValueError()


async def entered_email(
        message: Message,
        widget: ManagedTextInput[str],
        dialog_manager: DialogManager,
        email: str,
):
    user_id = message.from_user.id
    spreadsheet_id = await Database().get_spreadsheet_id(db, user_id)
    response_msg = share_access_sync(email, spreadsheet_id)

    await message.answer(response_msg)

    cash_flow_help = await get_message("cash_flow.help")
    await message.answer(cash_flow_help)

    await dialog_manager.done()
    await dialog_manager.start(SGCashFlow.cash_flow)
