from aiogram.types import Message
from aiogram import Router
from aiogram.filters import CommandStart
from database.models import User
from database import SessionLocal


start_router = Router()


@start_router.message(CommandStart())
async def handle_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name or "anonymous user"

    db = SessionLocal()
    try:
        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            user = User(id=user_id, username=username)
            db.add(user)
            db.commit()
            await message.answer(f"Welcome, {username}!")
        else:
            await message.answer(f"Welcome back, {username}!")
    finally:
        db.close()
        await message.answer("You can use /add_income or /add_spending to get started.")

