from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from database.redis import set_state, clear_state, set_temp_income, get_temp_income
from telegram_bot.keyboards.reply import confirm_keyboard
from database.models import DailyStats
from database import SessionLocal
import datetime
from config.config import logger
from telegram_bot.handlers.manage_start import i18n


async def start_income(message: types.Message, user_id):
    await set_state(user_id, "awaiting_income")
    return await message.answer(
        await i18n.get(
            key="messages.income.awaiting_income",
            user_id=user_id
        ))


async def handle_income_value(message: types.Message, user_id):
    try:
        income = float(message.text.strip())
    except ValueError:
        return await message.answer(
            await i18n.get(
                key="messages.error.ValueError",
                user_id=user_id
            ))

    await set_temp_income(user_id, income)
    await set_state(user_id, "confirm_income")

    return await message.answer(
        await i18n.get(
            key="messages.income.confirm",
            income=income,
            user_id=user_id
        ),
        reply_markup=await confirm_keyboard(user_id=user_id)
    )


async def handle_income_confirmation(message: types.Message, user_id):
    text = message.text
    db = SessionLocal()

    yes = await i18n.get(key="messages.confirm.yes", user_id=user_id)
    no = await i18n.get(key="messages.confirm.no", user_id=user_id)

    try:
        if text == yes:
            income = await get_temp_income(user_id)
            today = datetime.date.today()

            stats = DailyStats.get_or_create(db, user_id, today)
            try:
                if stats.income is None:
                    stats.income = 0.0
                stats.income += income
                stats.recalculate_total()

                db.commit()

            except Exception as e:
                logger.error("Database exception:", e)
            finally:
                db.close()

            await clear_state(user_id)
            return await message.answer(
                await i18n.get(
                    key="messages.income.success",
                    income=income,
                    user_id=user_id
                ),
                reply_markup=ReplyKeyboardRemove()
            )

        elif text == no:
            await clear_state(user_id)
            return await message.answer(
                await i18n.get(
                    key="messages.cancel",
                    user_id=user_id
                ),
                reply_markup=ReplyKeyboardRemove()
            )

        else:
            return await message.answer(
                await i18n.get(
                    key="messages.error.nonexistent",
                    user_id=user_id
                ))

    except Exception as e:
        logger.error("Exception:", e)
        return None
