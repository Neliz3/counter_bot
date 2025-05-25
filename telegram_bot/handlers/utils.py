from sqlalchemy import func
import datetime
from calendar import monthrange
from database.models import Spending, DailyStats
from config.config import logger


async def get_today_stats(session, user_id):
    today = datetime.date.today()
    year, month = today.year, today.month
    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month, monthrange(year, month)[1])

    # Spending grouped by category
    spending_data = (
        session.query(Spending).filter_by(user_id=user_id, date=today)
        .order_by(Spending.amount.desc())
        .limit(7)
        .all())

    # Total spent today from Spending
    total_spent = (
                      session.query(func.sum(Spending.amount))
                      .filter(Spending.user_id == user_id, Spending.date == today)
                      .scalar()
                  ) or 0.0


    # Total income for this month
    total_month_income = (
        session.query(func.sum(DailyStats.income))
        .filter(
            DailyStats.user_id == user_id,
            DailyStats.date >= start_date,
            DailyStats.date <= end_date
        )
        .scalar()
    ) or 0.0

    # Remaining = all income for the month - today’s spending
    remaining = total_month_income - total_spent

    return spending_data, total_spent, remaining


async def get_monthly_stats(session, user_id, year, month):
    # Get the first and the last day of the month
    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month, monthrange(year, month)[1])

    # Spending grouped by category
    spending_data = (
        session.query(Spending.category, func.sum(Spending.amount))
        .filter(
            Spending.user_id == user_id,
            Spending.date >= start_date,
            Spending.date <= end_date
        )
        .group_by(Spending.category)
        .order_by(func.sum(Spending.amount).desc())
        .limit(7)
        .all()
    )

    # Total income and spending from DailyStats
    totals = (
        session.query(
            func.sum(DailyStats.income),
            func.sum(DailyStats.spending)
        )
        .filter(
            DailyStats.user_id == user_id,
            DailyStats.date >= start_date,
            DailyStats.date <= end_date
        )
        .first()
    )

    total_income = totals[0] or 0.0
    total_spending = totals[1] or 0.0

    return spending_data, total_income, total_spending
