from aiogram import Router
from aiogram.types import Message
import datetime
from aiogram.filters import Command
from database import SessionLocal
from prettytable import PrettyTable
from telegram_bot.handlers.utils import get_today_stats, get_monthly_stats
from config.config import logger


statistics_router = Router()


@statistics_router.message(Command("today"))
async def handle_today_stats(message: Message):
    user_id = message.from_user.id
    today = datetime.date.today()

    with SessionLocal() as session:
        spending_data, total_spent, remaining = await get_today_stats(session, user_id)
        today_name = today.strftime("%B %d")

        if not spending_data:
            expenses_block = "No expenses recorded today."
        else:
            # Pretty output
            today_table = PrettyTable()
            today_table.title = f"Today Summary ~ {today_name}"

            today_table.field_names = ['Category', 'Amount']
            for s in spending_data:
                today_table.add_row([f'{s.description[:20]}\n({s.category[:20]})', s.amount])
            today_table.add_divider()
            today_table.add_row(['❌ Total Spending', total_spent])
            today_table.add_divider()
            today_table.add_row(['📌 Remaining', remaining])
            today_table.align['Category'] = 'l'
            today_table.align['Amount'] = 'r'

            expenses_block = today_table.get_string()

        await message.answer(f"<code>{expenses_block}</code>", parse_mode="HTML")


@statistics_router.message(Command("month"))
async def show_month_stats(message: Message):
    user_id = message.from_user.id
    now = datetime.datetime.now()

    with SessionLocal() as session:
        spending_data, total_income, total_spending = await get_monthly_stats(session, user_id, now.year, now.month)
        month_name = now.strftime("%B")
        remaining = total_income - total_spending or 0.0
        remaining_percent = (remaining / total_income) * 100 if total_income else 0.0

        if not spending_data:
            expenses_block = "No expenses recorded today."
        else:
            # Pretty output
            month_table = PrettyTable()
            month_table.title = f"Monthly Summary ~ {month_name}"

            month_table.field_names = ['Category', 'Amount', '% of Total']

            for s in spending_data:
                cat = s[0]
                amount = s[1]
                percentage = (amount / total_spending * 100) if total_spending else 0

                month_table.add_row([
                    f'{cat[:20]}',
                    f'{amount:7.1f}',
                    f'{percentage:5.1f}%'
                ])

            month_table.add_divider()
            month_table.add_row(['💰 Total Income', total_income, ''])
            month_table.add_divider()
            month_table.add_row(['❌ Total Spending', total_spending, ''])
            month_table.add_divider()
            month_table.add_row(['📌 Remaining', remaining, f"{remaining_percent:.1f}%"])
            month_table.align['Category'] = 'l'
            month_table.align['Amount'] = 'r'
            month_table.align['% of Total '] = 'r'

            month_table.padding_width = 0 # TODO: check on the phone, if not - use <pre> tag
            expenses_block = month_table.get_string()

        await message.answer(f"<code>{expenses_block}</code>", parse_mode="HTML")
