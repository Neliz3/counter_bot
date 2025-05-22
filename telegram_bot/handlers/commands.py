from aiogram import types, Router
from aiogram.filters import Command, CommandStart
from telegram_bot.handlers import add_income as ai, manage_start as ms
from database.redis import get_state
from config.config import logger


command_router = Router()


@command_router.message(Command("add_income"))
async def handle_add_income(message: types.Message):
    await ai.start_income(message)


@command_router.message()
async def handle_text_input(message: types.Message):
    state = await get_state(message.from_user.id)

    try:
        if state == "awaiting_income":
            await ai.handle_income_value(message)
        elif state == "confirm_income":
            await ai.handle_income_confirmation(message)
        else:
            await message.answer("I didn’t understand that.")
    except Exception as e:
        logger.error("Exception:", e)


@command_router.message(CommandStart)
async def handle_start_command(message: types.Message):
    await ms.handle_start(message)
