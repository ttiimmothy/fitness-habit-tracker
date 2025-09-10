import uuid
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc

from app.api.dependencies.get_current_user import get_current_user
from app.db.session import get_db
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.models.user import User
from app.services.analytics import build_week_overview
from app.schemas.common import DailyLogCount, HabitStats, HabitDailyProgress

router = APIRouter()


@router.get("/overview", response_model=dict)
def overview(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  habit_ids = [h.id for h in db.query(Habit.id).filter(Habit.user_id == current_user.id).all()]
  logs = db.query(HabitLog).filter(HabitLog.habit_id.in_(habit_ids)).all() if habit_ids else []
  return build_week_overview(logs)

@router.get("/daily-counts", response_model=list[DailyLogCount])
def get_daily_log_counts(
    days: int = Query(default=30, ge=1, le=365,
                      description="Number of days to look back"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
  """Get daily habit log counts for the user's habits over the specified number of days."""
  end_date = date.today()
  start_date = end_date - timedelta(days=days-1)

  # Get all habits for the user
  user_habits = db.query(Habit.id).filter(
      Habit.user_id == current_user.id).subquery()

  # Query daily log counts
  daily_counts = db.query(
      HabitLog.date,
      func.count(HabitLog.id).label('count')
  ).join(
      user_habits, HabitLog.habit_id == user_habits.c.id
  ).filter(
      and_(
          HabitLog.date >= start_date,
          HabitLog.date <= end_date
      )
  ).group_by(
      HabitLog.date
  ).order_by(
      HabitLog.date
  ).all()

  # Convert to dict for easier lookup
  counts_dict = {row.date: row.count for row in daily_counts}

  # Fill in missing dates with 0 counts
  result = []
  current_date = start_date
  while current_date <= end_date:
    count_value = counts_dict.get(current_date, 0)
    # Ensure count is an integer
    count = count_value if isinstance(count_value, int) else 0
    result.append(DailyLogCount(date=current_date, count=count))
    current_date += timedelta(days=1)

  return result


@router.get("/{habit_id}/stats/steak", response_model=HabitStats)
def get_habit_stats_streak(
    habit_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
  """Get statistics for a specific habit."""
  habit = db.query(Habit).filter(Habit.id == uuid.UUID(
      habit_id), Habit.user_id == current_user.id).first()

  if not habit:
    raise HTTPException(status_code=404, detail="Habit not found")

  # Get total logs count
  total_logs = db.query(func.count(HabitLog.id)).filter(
      HabitLog.habit_id == habit.id).scalar() or 0

  # Get all logs ordered by date
  logs = db.query(HabitLog.date).filter(
      HabitLog.habit_id == habit.id
  ).order_by(HabitLog.date.desc()).all()

  log_dates = [log.date for log in logs]

  # Calculate streaks
  current_streak = 0
  longest_streak = 0
  temp_streak = 0
  last_log_date = log_dates[0] if log_dates else None

  if log_dates:
    # Calculate current streak (consecutive days from today backwards)
    today = date.today()
    current_date = today

    for log_date in log_dates:
      if log_date == current_date:
        current_streak += 1
        current_date -= timedelta(days=1)
      elif log_date < current_date:
        break

    # Calculate longest streak
    if len(log_dates) > 1:
      temp_streak = 1
      for i in range(1, len(log_dates)):
        if (log_dates[i-1] - log_dates[i]).days == 1:
          temp_streak += 1
        else:
          longest_streak = max(longest_streak, temp_streak)
          temp_streak = 1
      longest_streak = max(longest_streak, temp_streak)
    else:
      longest_streak = 1

  # Calculate completion rate
  # For daily habits, calculate based on days since creation
  # For weekly habits, calculate based on weeks since creation
  if habit.frequency.value == "daily":
    days_since_creation = (date.today() - habit.created_at.date()).days + 1
    completion_rate = (total_logs / days_since_creation) * \
        100 if days_since_creation > 0 else 0
  elif habit.frequency.value == "weekly":
    weeks_since_creation = (
        (date.today() - habit.created_at.date()).days // 7) + 1
    completion_rate = (total_logs / weeks_since_creation) * \
        100 if weeks_since_creation > 0 else 0
  else:  # monthly
    months_since_creation = (
        (date.today() - habit.created_at.date()).days // 30) + 1
    completion_rate = (total_logs / months_since_creation) * \
        100 if months_since_creation > 0 else 0

  return HabitStats(
    habit_id=str(habit.id),
    current_streak=current_streak,
    longest_streak=longest_streak
    # total_logs=total_logs,
    # completion_rate=round(completion_rate, 2),
    # last_log_date=last_log_date
  )


@router.get("/{habit_id}/daily-progress", response_model=list[HabitDailyProgress])
def get_habit_daily_progress(
    habit_id: str,
    days: int = Query(default=7, ge=1, le=365,
                      description="Number of days to look back"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
  """Get daily progress for a specific habit over the specified number of days."""
  habit = db.query(Habit).filter(Habit.id == uuid.UUID(
      habit_id), Habit.user_id == current_user.id).first()

  if not habit:
    raise HTTPException(status_code=404, detail="Habit not found")

  end_date = date.today()
  start_date = end_date - timedelta(days=days-1)

  # Get all logs for this habit in the date range
  logs = db.query(HabitLog.date).filter(
      and_(
          HabitLog.habit_id == habit.id,
          HabitLog.date >= start_date,
          HabitLog.date <= end_date
      )
  ).all()

  # Convert to set for faster lookup
  logged_dates = {log.date for log in logs}

  # Generate progress data for each day
  result = []
  current_date = start_date
  while current_date <= end_date:
    # Check if habit was completed on this date
    completed = current_date in logged_dates
    actual = 1 if completed else 0

    result.append(HabitDailyProgress(
        date=current_date,
        completed=completed,
        target=habit.target,
        actual=actual
    ))
    current_date += timedelta(days=1)

  return result

