from aiogram.types import Message
from database.models import User
from database import SessionLocal


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
            await message.answer(f"Welcome, {username}! You’ve been registered.")
        else:
            await message.answer(f"Welcome back, {username}!")
    finally:
        db.close()
