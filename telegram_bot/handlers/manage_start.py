from aiogram.types import Message
from aiogram import Router
from aiogram.filters import CommandStart
from database.models import User
from database import SessionLocal
from database.mongo import initialize_user_categories
from database.redis import set_user_lang, clear_user_lang
from config.config import DEFAULT_LANG, LANGUAGES
from telegram_bot.utils.i18n import I18n


start_router = Router()
i18n = I18n()


@start_router.message(CommandStart())
async def handle_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name or "🥳"

    # Store user language
    user_lang = message.from_user.language_code
    user_lang = user_lang if user_lang in LANGUAGES else DEFAULT_LANG

    await clear_user_lang(user_id)
    await set_user_lang(user_id, user_lang)

    db = SessionLocal()
    try:
        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            user = User(id=user_id, username=username)
            db.add(user)
            db.commit()

            await initialize_user_categories(user_id=user_id, lang=user_lang)

            await message.answer(
                await i18n.get(
                    key="messages.start.welcome",
                    user_id=user_id,
                    name=username
                ))
        else:
            await message.answer(
                await i18n.get(
                    key="messages.start.welcome_back",
                    user_id=user_id,
                    name=username
                ))
    finally:
        db.close()

        await message.answer(
            await i18n.get(
                key="messages.start.help",
                user_id=user_id
            ))
