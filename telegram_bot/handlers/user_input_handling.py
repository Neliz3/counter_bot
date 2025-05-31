from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove
from telegram_bot.handlers import add_income as ai, add_spending as asp
from config.config import logger
from database.redis import get_state, clear_state
from telegram_bot.handlers.manage_start import i18n
from telegram_bot.filters.text_i18n import TextI18nFilter


user_input_router = Router()


@user_input_router.message(Command("add_income"))
async def handle_add_income(message: types.Message):
    await ai.start_income(message, message.from_user.id)


@user_input_router.message(Command("add_spending"))
async def handle_add_spending(message: types.Message):
    await asp.start_spending(message, message.from_user.id)


@user_input_router.message(TextI18nFilter("buttons.cancel"))
async def handle_cancel(message: types.Message):
    user_id = message.from_user.id

    await clear_state(user_id)
    await message.answer(
        await i18n.get(key="messages.cancel", user_id=message.from_user.id),
        reply_markup=ReplyKeyboardRemove()
    )

    await message.delete()

    await message.answer(
        await i18n.get(key="messages.start.help", user_id=user_id),
    )


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
            await message.answer(
                await i18n.get(
                    key="messages.error.default",
                    user_id=user_id
                )
            )
    except Exception as e:
        logger.error("Exception: %s", str(e))
