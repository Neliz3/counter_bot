from aiogram import Router
from aiogram.types import Message
from sqlalchemy.orm import Session
from sqlalchemy import func
import datetime
from aiogram.filters import Command
from database import SessionLocal
from database.models import Spending, DailyStats
from prettytable import PrettyTable

statistics_router = Router()


@statistics_router.message(Command("today"))
async def handle_today_stats(message: Message):
    user_id = message.from_user.id
    today = datetime.date.today()
    db: Session = SessionLocal()

    try:
        spending = (db.query(Spending).filter_by(user_id=user_id, date=today).
                    order_by(Spending.amount.desc()).limit(5).all())

        total_spent = (
            db.query(func.sum(Spending.amount))
            .filter(Spending.user_id == user_id, Spending.date == today)
            .scalar()
        ) or 0.0

        stats = DailyStats.get_or_create(db, user_id=user_id, date=today)
        db.commit()

        if not spending:
            expenses_block = "No expenses recorded today."
        else:
            today_table = PrettyTable()
            today_table.field_names = ['Category', 'Amount']
            today_table.title = f"Today's Expenses ~ {today.strftime('%B %d')}"
            for s in spending:
                today_table.add_row([f'{s.description[:20]}\n({s.category[:20]})', s.amount])
            today_table.add_divider()
            today_table.add_row(['❌ Total spent', total_spent])
            today_table.add_divider()
            today_table.add_row(['📌 Remains', stats.total])
            today_table.align['Category'] = 'l'
            today_table.align['Amount'] = 'r'

            expenses_block = today_table.get_string()

        await message.answer(f"<code>{expenses_block}</code>", parse_mode="HTML")

    finally:
        db.close()
