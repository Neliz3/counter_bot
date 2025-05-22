from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
import datetime
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)

    stats = relationship("DailyStats", back_populates="user", cascade="all, delete-orphan")


class DailyStats(Base):
    __tablename__ = 'daily_stats'
    __table_args__ = (
        UniqueConstraint('user_id', 'date', name='user_date_uc'),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date, default=datetime.date.today)

    income = Column(Float, default=0.0)
    spendings = Column(Float, default=0.0)
    total = Column(Float, default=0.0)

    user = relationship("User", back_populates="stats")

    def recalculate_total(self):
        if self.income is None:
            self.income = 0.0
        if self.spendings is None:
            self.spendings = 0.0
        self.total = self.income - self.spendings

    @staticmethod
    def get_or_create(session, user_id, date):
        stats = session.query(DailyStats).filter_by(user_id=user_id, date=date).first()
        if not stats:
            stats = DailyStats(user_id=user_id, date=date)
            session.add(stats)
        return stats
