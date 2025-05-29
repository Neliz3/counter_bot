from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from database.redis import (set_state, clear_state,
                            set_temp_spending, get_temp_spending,
                            set_temp_desc, get_temp_desc,
                            get_temp_cat, set_temp_cat)
from telegram_bot.keyboards.reply import confirm_keyboard, cancel_button
from database import SessionLocal
from config.config import logger
from telegram_bot.ai_cat_detection.classifier import get_category
from database.utils import add_spending
from telegram_bot.handlers.manage_start import i18n


async def start_spending(message: types.Message, user_id):
    await set_state(user_id, "awaiting_spending_desc")
    return await message.answer(
        await i18n.get(
            key="messages.spending.awaiting_spending_desc",
            user_id=user_id
        ),
        reply_markup=await cancel_button(user_id)
    )


async def handle_spending_desc(message: types.Message, user_id):
    desc = message.text
    await set_temp_desc(user_id, desc)
    await set_state(user_id, "awaiting_spending_amount")

    await message.answer(
        await i18n.get(
            key="messages.spending.awaiting_spending_amount",
            desc=desc,
            user_id=user_id
        ),
        parse_mode='Markdown',
        reply_markup=await cancel_button(user_id)
    )

    cat = await get_category(user_id, desc)
    await set_temp_cat(user_id, cat)


async def handle_spending_value(message: types.Message, user_id):
    try:
        amount = float(message.text)
    except ValueError:
        return await message.answer(
            await i18n.get(
                key="messages.error.ValueError",
                user_id=user_id
            ),
            reply_markup=await cancel_button(user_id)
        )

    await set_temp_spending(user_id, amount)
    desc = await get_temp_desc(user_id)
    await set_state(user_id, "confirm_spending")

    return await message.answer(
        await i18n.get(
            key="messages.spending.confirm",
            amount=amount,
            desc=desc,
            user_id=user_id
        ),
        reply_markup=await confirm_keyboard(user_id=user_id),
        parse_mode='Markdown'
    )


async def handle_spending_confirmation(message: types.Message, user_id: int):
    text = message.text
    db = SessionLocal()

    yes = await i18n.get(key="messages.confirm.yes", user_id=user_id)
    no = await i18n.get(key="messages.confirm.no", user_id=user_id)

    try:
        if text == yes:
            amount = await get_temp_spending(user_id)
            desc = await get_temp_desc(user_id)
            cat = await get_temp_cat(user_id)

            try:
                await add_spending(db, user_id, amount, description=desc, category=cat)
            except Exception as e:
                logger.error("Database exception:", e)
            finally:
                db.close()

            await message.answer(
                await i18n.get(
                    key="messages.spending.success",
                    amount=amount,
                    cat=cat,
                    user_id=user_id
                ),
                reply_markup=ReplyKeyboardRemove(),
                parse_mode='Markdown'
            )

            await clear_state(user_id)
            return None

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
