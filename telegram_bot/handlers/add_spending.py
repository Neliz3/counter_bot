from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from database.redis import (set_state, clear_state,
                            set_temp_spending, get_temp_spending, set_temp_desc, get_temp_desc, get_temp_cat, set_temp_cat)
from telegram_bot.keyboards.reply import confirm_keyboard
from database import SessionLocal
from config.config import logger
from telegram_bot.ai_cat_detection.classifier import get_category
from database.utils import add_spending


async def start_spending(message: types.Message, user_id):
    await set_state(user_id, "awaiting_spending_desc")
    await message.answer(f'What did you spend on?')


async def handle_spending_desc(message: types.Message, user_id):
    desc = message.text
    await set_temp_desc(user_id, desc)
    await set_state(user_id, "awaiting_spending_amount")

    await message.answer(f'How much did you spend on `{desc}`?')
    cat = await get_category(user_id, desc)
    await set_temp_cat(user_id, cat)


async def handle_spending_value(message: types.Message, user_id):
    try:
        amount = float(message.text)
    except ValueError:
        await message.answer("Please enter a valid number.")
        return

    await set_temp_spending(user_id, amount)
    desc = await get_temp_desc(user_id)
    await set_state(user_id, "confirm_spending")

    await message.answer(
        f'You spent {amount} on "{desc}". Confirm?',
        reply_markup=confirm_keyboard()
    )


async def handle_spending_confirmation(message: types.Message, user_id: int):
    text = message.text.lower()
    db = SessionLocal()

    try:
        if text == "yes":
            amount = await get_temp_spending(user_id)
            desc = await get_temp_desc(user_id)
            cat = await get_temp_cat(user_id)

            try:
                await add_spending(db, user_id, amount, description=desc, category=cat)
            except Exception as e:
                logger.error("Database exception:", e)
            finally:
                db.close()

            await message.answer(f"✅ {cat}: -{amount}", reply_markup=ReplyKeyboardRemove())
            await clear_state(user_id)
            return None

        elif text == "no":
            await clear_state(user_id)
            await message.answer("Canceled.", reply_markup=ReplyKeyboardRemove())
            return None
        else:
            await message.answer("Please type Yes or No.")
            return None
    except Exception as e:
        logger.error("Exception:", e)
        return None
