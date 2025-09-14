from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.user import User
from app.models.habit import Habit, Frequency
from app.models.habit_log import HabitLog


def seed() -> None:
  Base.metadata.create_all(bind=engine)
  db: Session = SessionLocal()
  try:
    demo = db.query(User).filter(User.email == "demo@example.com").first()
    if not demo:
      demo = User(email="demo@example.com", password_hash=hash_password("12"), name="Demo User")
      db.add(demo)
      db.commit()
      db.refresh(demo)

    daily = db.query(Habit).filter(Habit.user_id == demo.id, Habit.title == "Daily Walk").first()
    if not daily:
      daily = Habit(user_id=demo.id, title="Daily Walk", frequency=Frequency.daily, target=1)
      db.add(daily)

    weekly = db.query(Habit).filter(Habit.user_id == demo.id, Habit.title == "Gym Sessions").first()
    if not weekly:
      weekly = Habit(user_id=demo.id, title="Gym Sessions", frequency=Frequency.weekly, target=3)
      db.add(weekly)

    db.commit()
    db.refresh(daily)
    db.refresh(weekly)

    # logs for last 14 days for daily
    # start = date.today() - timedelta(days=14)
    # for i in range(15):
    #   d = start + timedelta(days=i)
    #   if i % 2 == 0:
    #     if not db.query(HabitLog).filter(HabitLog.habit_id == daily.id, HabitLog.date == d).first():
    #       db.add(HabitLog(habit_id=daily.id, date=d))

    # # logs for last 4 weeks for weekly (every Tue/Thu)
    # for i in range(28):
    #   d = date.today() - timedelta(days=i)
    #   if d.weekday() in (1, 3):
    #     if not db.query(HabitLog).filter(HabitLog.habit_id == weekly.id, HabitLog.date == d).first():
    #       db.add(HabitLog(habit_id=weekly.id, date=d))

    db.commit()
  finally:
    db.close()


if __name__ == "__main__":
  seed()
