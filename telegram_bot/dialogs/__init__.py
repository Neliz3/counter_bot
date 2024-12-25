"""
Dialog -> windows -> widgets
Widget = [text, keyboard, media, input, link preview]
"""

from . import getters
from . import states
from . import utils
from . import windows
from aiogram_dialog import Dialog, setup_dialogs
from aiogram import Dispatcher

async def dialogs():
    return [
        Dialog(
            await windows.email_window()
        )
    ]

async def register_dialogs(dp: Dispatcher):
    for dialog in await dialogs():
        dp.include_router(dialog)
    setup_dialogs(dp)
