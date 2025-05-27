from aiogram import Router
from aiogram.types import Message
import datetime
from aiogram.filters import Command
from database import SessionLocal
from prettytable import PrettyTable
from telegram_bot.handlers.utils import get_today_stats, get_monthly_stats
from telegram_bot.handlers.manage_start import i18n
from telegram_bot.handlers.utils import get_localized_date
from database.redis import get_user_lang


statistics_router = Router()


@statistics_router.message(Command("today"))
async def handle_today_stats(message: Message):
    user_id = message.from_user.id
    today = datetime.date.today()
    today_name = get_localized_date(date=today, user_lang=await get_user_lang(user_id))

    with SessionLocal() as session:
        spending_data, total_spent, remaining = await get_today_stats(session, user_id)

        if not spending_data:
            expenses_block = await i18n.get(
                key="messages.statistics.error",
                user_id=user_id
            )
        else:
            title_today_str = await i18n.get(
                key="messages.statistics.title_today",
                today_name=today_name,
                user_id=user_id)
            category_str = await i18n.get(key="messages.statistics.category", user_id=user_id)
            amount_str = await i18n.get(key="messages.statistics.amount", user_id=user_id)
            total_spent_str = await i18n.get(key="messages.statistics.total_spent", user_id=user_id)
            remaining_str = await i18n.get(key="messages.statistics.remaining", user_id=user_id)

            # Pretty output
            today_table = PrettyTable()
            today_table.title = title_today_str

            today_table.field_names = [category_str, amount_str]
            for s in spending_data:
                today_table.add_row([f'{s.description[:20]}\n({s.category[:20]})', s.amount])
            today_table.add_divider()
            today_table.add_row([total_spent_str, total_spent])
            today_table.add_divider()
            today_table.add_row([remaining_str, remaining])
            today_table.align[category_str] = 'l'
            today_table.align[amount_str] = 'c'

            expenses_block = today_table.get_string()

        await message.answer(f"<code>{expenses_block}</code>", parse_mode="HTML")


@statistics_router.message(Command("month"))
async def show_month_stats(message: Message):
    user_id = message.from_user.id
    now = datetime.datetime.now()

    with SessionLocal() as session:
        spending_data, total_income, total_spending = await get_monthly_stats(session, user_id, now.year, now.month)
        month_name = get_localized_date(date=now, user_lang=await get_user_lang(user_id))
        remaining = total_income - total_spending or 0.0
        remaining_percent = (remaining / total_income) * 100 if total_income else 0.0

        if not spending_data:
            expenses_block = await i18n.get(
                key="messages.statistics.error",
                user_id=user_id
            )
        else:
            title_month_str = await i18n.get(
                key="messages.statistics.title_month",
                month_name=month_name,
                user_id=user_id)
            category_str = await i18n.get(key="messages.statistics.category", user_id=user_id)
            amount_str = await i18n.get(key="messages.statistics.amount", user_id=user_id)
            total_income_str = await i18n.get(key="messages.statistics.total_income", user_id=user_id)
            total_spent_str = await i18n.get(key="messages.statistics.total_spent", user_id=user_id)
            percentage_str = await i18n.get(key="messages.statistics.percentage", user_id=user_id)
            remaining_str = await i18n.get(key="messages.statistics.remaining", user_id=user_id)

            # Pretty output
            month_table = PrettyTable()
            month_table.title = title_month_str

            month_table.field_names = [category_str, amount_str, percentage_str]

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
            month_table.add_row([total_income_str, total_income, ''])
            month_table.add_divider()
            month_table.add_row([total_spent_str, total_spending, ''])
            month_table.add_divider()
            month_table.add_row([remaining_str, remaining, f"{remaining_percent:.1f}%"])
            month_table.align[category_str] = 'l'
            month_table.align[amount_str] = 'c'
            month_table.align[percentage_str] = 'c'

            month_table.padding_width = 0 # TODO: check on the phone, if not - use <pre> tag
            expenses_block = month_table.get_string()

        await message.answer(f"<code>{expenses_block}</code>", parse_mode="HTML")
