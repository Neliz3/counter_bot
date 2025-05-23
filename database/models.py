from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
import datetime
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)

    stats = relationship("DailyStats", back_populates="user", cascade="all, delete-orphan")
    spending = relationship("Spending", backref="user", cascade="all, delete-orphan")


class Spending(Base):
    __tablename__ = "spending"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"), nullable=False)
    date = Column(Date, default=datetime.date.today())
    amount = Column(Float, nullable=False, default=0.0)
    category = Column(String, nullable=True)      # Optional: Food, Transport, etc.
    description = Column(String, nullable=True)   # E.g. "coffee", "uber"


class DailyStats(Base):
    __tablename__ = 'daily_stats'
    __table_args__ = (
        UniqueConstraint('user_id', 'date', name='user_date_uc'),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date, default=datetime.date.today)
    spending = Column(Float, default=0.0)
    income = Column(Float, default=0.0)
    total = Column(Float, default=0.0)

    user = relationship("User", back_populates="stats")

    def recalculate_total(self):
        if self.income is None:
            self.income = 0.0
        if self.spending is None:
            self.spending = 0.0
        self.total = self.income - self.spending

    @staticmethod
    def get_or_create(session, user_id, date):
        stats = session.query(DailyStats).filter_by(user_id=user_id, date=date).first()
        if not stats:
            stats = DailyStats(user_id=user_id, date=date)
            session.add(stats)
        return stats
