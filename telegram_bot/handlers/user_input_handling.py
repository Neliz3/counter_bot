from aiogram import types, Router
from aiogram.filters import Command
from telegram_bot.handlers import add_income as ai, add_spending as asp
from config.config import logger
from database.redis import get_state


user_input_router = Router()


@user_input_router.message(Command("add_income"))
async def handle_add_income(message: types.Message):
    await ai.start_income(message, message.from_user.id)


@user_input_router.message(Command("add_spending"))
async def handle_add_spending(message: types.Message):
    await asp.start_spending(message, message.from_user.id)


@user_input_router.message()
async def handle_text_input(message: types.Message):
    user_id = message.from_user.id
    state = await get_state(user_id)

    try:
        # ===== Income logic =====
        if state == "awaiting_income":
            await ai.handle_income_value(message, user_id)
        elif state == "confirm_income":
            await ai.handle_income_confirmation(message, user_id)

        # ===== Spending logic =====
        elif state == "awaiting_spending_desc":
            await asp.handle_spending_desc(message, user_id)
        elif state == "awaiting_spending_amount":
            await asp.handle_spending_value(message, user_id)
        elif state == "confirm_spending":
            await asp.handle_spending_confirmation(message, user_id)
        else:
            await message.answer("I don’t understand that.")
    except Exception as e:
        logger.error("Exception: %s", str(e))
