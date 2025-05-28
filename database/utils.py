from database.models import DailyStats, Spending
import datetime


async def add_spending(
        session, user_id: int, amount: float, date=None, category=None, description=None
) -> None:
    date = date or datetime.date.today()

    # Add spending record
    spending = Spending(
        user_id=user_id, amount=amount, date=date, category=category, description=description
    )
    session.add(spending)

    # Update or create daily_stats
    stats = DailyStats.get_or_create(session, user_id, date)
    if stats.spending is None:
        stats.spending = 0.0
    stats.spending += amount
    stats.recalculate_total()

    session.commit()

    return None
