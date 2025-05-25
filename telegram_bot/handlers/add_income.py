from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from database.redis import set_state, clear_state, set_temp_income, get_temp_income
from telegram_bot.keyboards.reply import confirm_keyboard
from database.models import DailyStats
from database import SessionLocal
import datetime
from config.config import logger


async def start_income(message: types.Message, user_id):
    await set_state(user_id, "awaiting_income")
    await message.answer("How much did you earn?")


async def handle_income_value(message: types.Message, user_id):
    try:
        income = float(message.text.strip())
    except ValueError:
        return await message.answer("Please enter a valid number.")

    await set_temp_income(user_id, income)
    await set_state(user_id, "confirm_income")

    await message.answer(
        f"You entered {income}. Confirm?",
        reply_markup=confirm_keyboard()
    )
    return None


async def handle_income_confirmation(message: types.Message, user_id):
    text = message.text.lower()
    db = SessionLocal()

    try:
        if text == "yes":
            income = await get_temp_income(user_id)
            today = datetime.date.today()

            stats = DailyStats.get_or_create(db, user_id, today)
            try:
                if stats.income is None:
                    stats.income = 0.0
                stats.income += income
            except Exception as e:
                logger.error("Exception of stats.income:", e)
            stats.recalculate_total()

            db.commit()
            await clear_state(user_id)
            return await message.answer(
                f"✅ Saved {income} as income",
                reply_markup=ReplyKeyboardRemove())

        elif text == "no":
            await clear_state(user_id)
            return await message.answer(
                "Canceled.",
                reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer("Please type Yes or No.")
            return None
    except Exception as e:
        logger.error("Exception:", e)
    finally:
        db.close()
