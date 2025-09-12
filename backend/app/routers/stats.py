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
from app.schemas.stats import TodayHabitLog, DailyLogCount, HabitStats, HabitDailyProgress
from app.services.analytics import build_week_overview

router = APIRouter()


@router.get("/overview", response_model=dict)
def overview(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  habit_ids = [h.id for h in db.query(Habit.id).filter(
      Habit.user_id == current_user.id).all()]
  logs = db.query(HabitLog).filter(
      HabitLog.habit_id.in_(habit_ids)).all() if habit_ids else []
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


@router.get("/{habit_id}/stats/streak", response_model=HabitStats)
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

  # Get all logs ordered by date with quantities
  logs = db.query(HabitLog.date, HabitLog.quantity).filter(
      HabitLog.habit_id == habit.id
  ).order_by(HabitLog.date.desc()).all()

  # Filter logs where quantity >= target (successful completion)
  successful_logs = [log for log in logs if log.quantity >= habit.target]
  successful_dates = [log.date for log in successful_logs]

  # Calculate streaks based on successful completions
  current_streak = 0
  longest_streak = 0
  temp_streak = 0
  last_log_date = successful_dates[0] if successful_dates else None

  if successful_dates:
    # Calculate current streak (consecutive days from today backwards)
    today = date.today()
    current_date = today

    for log_date in successful_dates:
      if log_date == current_date:
        current_streak += 1
        current_date -= timedelta(days=1)
      elif log_date < current_date:
        break

    # Calculate longest streak
    if len(successful_dates) > 1:
      temp_streak = 1
      for i in range(1, len(successful_dates)):
        if (successful_dates[i-1] - successful_dates[i]).days == 1:
          temp_streak += 1
        else:
          longest_streak = max(longest_streak, temp_streak)
          temp_streak = 1
      longest_streak = max(longest_streak, temp_streak)
    else:
      longest_streak = 1

  # Calculate completion rate based on frequency
  if habit.frequency.value == "daily":
    # For daily habits: count unique successful days / total days
    unique_successful_dates = list(set(successful_dates))
    days_since_creation = (date.today() - habit.created_at.date()).days + 1
    completion_rate = (len(unique_successful_dates) / days_since_creation) * \
        100 if days_since_creation > 0 else 0
  elif habit.frequency.value == "weekly":
    # For weekly habits: count weeks with at least one successful completion
    weeks_since_creation = (
        (date.today() - habit.created_at.date()).days // 7) + 1

    # Group successful dates by week and count weeks with at least one success
    successful_weeks = set()
    for log_date in successful_dates:
      # Calculate which week this date falls into (weeks since habit creation)
      days_since_creation = (log_date - habit.created_at.date()).days
      week_number = days_since_creation // 7
      successful_weeks.add(week_number)

    completion_rate = (len(successful_weeks) / weeks_since_creation) * \
        100 if weeks_since_creation > 0 else 0
  else:  # monthly
    # For monthly habits: count months with at least one successful completion
    months_since_creation = (
        (date.today() - habit.created_at.date()).days // 30) + 1

    # Group successful dates by month and count months with at least one success
    successful_months = set()
    for log_date in successful_dates:
      # Calculate which month this date falls into (months since habit creation)
      days_since_creation = (log_date - habit.created_at.date()).days
      month_number = days_since_creation // 30
      successful_months.add(month_number)

    completion_rate = (len(successful_months) / months_since_creation) * \
        100 if months_since_creation > 0 else 0

  return HabitStats(
      habit_id=str(habit.id),
      current_streak=current_streak,
      longest_streak=longest_streak,
      # total_logs=total_logs,
      completion_rate=round(completion_rate, 2)
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

  # Get all logs for this habit in the date range with quantities
  logs = db.query(HabitLog.date, HabitLog.quantity).filter(
      and_(
          HabitLog.habit_id == habit.id,
          HabitLog.date >= start_date,
          HabitLog.date <= end_date
      )
  ).all()

  # Convert to dict for faster lookup with quantities
  logged_quantities = {log.date: log.quantity for log in logs}

  # Generate progress data for each day
  result = []
  current_date = start_date
  while current_date <= end_date:
    # Get actual quantity logged for this date
    actual_quantity = logged_quantities.get(current_date, 0)
    completed = actual_quantity >= habit.target

    result.append(HabitDailyProgress(
        date=current_date,
        completed=completed,
        target=habit.target,
        actual=actual_quantity
    ))
    current_date += timedelta(days=1)

  return result


@router.get("/logs/today", response_model=list[TodayHabitLog])
def get_today_habits_logs_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
  """Get all user's habits with their today's log status."""
  today = date.today()

  # Get all habits for the user
  habits = db.query(Habit).filter(Habit.user_id == current_user.id).all()

  if not habits:
    return []

  # Get all habit IDs
  habit_ids = [habit.id for habit in habits]

  # Get today's logs for all habits
  today_logs = db.query(HabitLog).filter(
      and_(
          HabitLog.habit_id.in_(habit_ids),
          HabitLog.date == today
      )
  ).all()

  # Sum quantities per habit for current_progress
  habit_log_counts = {}
  for log in today_logs:
    habit_log_counts[log.habit_id] = habit_log_counts.get(
        log.habit_id, 0) + log.quantity

  # Get the most recent log for each habit (for log_id and log_created_at)
  today_logs_dict = {}
  for log in today_logs:
    if log.habit_id not in today_logs_dict:
      today_logs_dict[log.habit_id] = log

  # Build response
  result = []
  for habit in habits:
    current_progress = habit_log_counts.get(habit.id, 0)
    logged_today = current_progress > 0
    today_log = today_logs_dict.get(habit.id)

    result.append(TodayHabitLog(
        habit_id=str(habit.id),
        title=habit.title,
        category=habit.category.value,
        frequency=habit.frequency.value,
        target=habit.target,
        logged_today=logged_today,
        current_progress=current_progress,
        log_id=str(today_log.id) if today_log else None,
        log_created_at=today_log.created_at if today_log else None
    ))

  return result