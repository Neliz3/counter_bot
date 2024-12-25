from typing import Any, Dict
from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import ManagedTextInput
import re


async def error(
        message: Message,
        dialog_: Any,
        manager: DialogManager,
        error_: ValueError
):
    await message.answer("❌ Please enter a valid email!")


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
    email = dialog_manager.find("email").get_value()
    if email:
        dialog_manager.dialog_data["email"] = email
        await dialog_manager.done(result={"email": email})
