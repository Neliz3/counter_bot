from database.db import database as db, Database
from telegram_bot.authentication.auth import user_connect
from google_sheets.auth import share_access_sync
from google_sheets.commands import get_expenses_value, get_pocket_value, get_categories
from aiogram.filters import CommandStart
from aiogram import html
from aiogram import Router
from aiogram.filters import Command
from aiogram_dialog import DialogManager, StartMode
from telegram_bot.dialogs.states import SGEmail, SGMain, SGFlow
from aiogram.types import Message
from telegram_bot.config import get_message
from telegram_bot.keyboards.reply import cash_flow_hint
import asyncio


router = Router()


@router.message(CommandStart())
async def command_start(message: Message, dialog_manager: DialogManager) -> None:
    """
    This handler receives messages with `/start` command
    """
    # await dialog_manager.start(SGMain.start, mode=StartMode.RESET_STACK)

    name = html.bold(message.from_user.first_name)

    await message.answer(await get_message("start.main", name=name))
    await message.answer(await get_message("start.wait"))

    user_id = message.from_user.id
    # TODO: optimize not to go to db each time (maybe temp db)
    spreadsheet_id = await Database().get_spreadsheet_id(db, user_id)

    await user_connect(user_id)

    await message.answer(await get_message("categories.main"))
    async for msg in get_categories(spreadsheet_id, pretty=True):
        await message.answer(msg)

    example_msg = await get_message("example")
    await message.answer(example_msg, reply_markup=cash_flow_hint)


@router.message(Command("pocket"))
async def command_pocket(message: Message):
    """
    This handler receives messages with `/pocket` command
    """
    user_id = message.from_user.id
    spreadsheet_id = await Database().get_spreadsheet_id(db, user_id)
    pocket_value = await get_pocket_value(spreadsheet_id)

    await message.answer(f'Pocket: {pocket_value}')


@router.message(Command("expenses"))
async def command_expenses(message: Message):
    """
    This handler receives messages with `/expenses` command
    """
    user_id = message.from_user.id
    spreadsheet_id = await Database().get_spreadsheet_id(db, user_id)
    expenses_value = await get_expenses_value(spreadsheet_id)

    await message.answer(f'Expenses for day: {expenses_value}')


@router.message(Command("table"))
async def command_share_sheet(message: Message, dialog_manager: DialogManager):
    """
    This handler receives messages with `/table` command
    """

    email = dialog_manager.dialog_data.get("email")
    print(f"Received email: {email}")

    if email:
        user_id = message.from_user.id

        spreadsheet_id = await Database().get_spreadsheet_id(db, user_id)
        response_msg = share_access_sync(email, spreadsheet_id)

        await message.answer(response_msg)
