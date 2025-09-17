import uuid
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc

from app.middleware.verify_token import verify_token
from app.db.session import get_db
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.models.habit_completion import HabitCompletion
from app.models.user import User
from app.schemas.stats import TodayHabitLog, DailyLogCount, HabitStats, HabitDailyProgress, DayLogs, HabitLogEntry
from app.services.completion_service import get_habit_streak_from_completions, get_habit_completion_stats

router = APIRouter()


@router.get("/overview/calendar", response_model=list[DayLogs])
def overview(db: Session = Depends(get_db), current_user: User = Depends(verify_token)):
  """Get comprehensive overview of all habit logs grouped by date"""
  # Get all habits for the user
  habits = db.query(Habit).filter(Habit.user_id == current_user.id).all()
  habit_ids = [h.id for h in habits]

  if not habit_ids:
    return []

  # Get all logs for user's habits, ordered by date and created_at
  logs = db.query(HabitLog).filter(
      HabitLog.habit_id.in_(habit_ids)
  ).order_by(HabitLog.date.desc(), HabitLog.created_at.desc()).all()

  # Group logs by date
  logs_by_date = {}
  for log in logs:
    log_date = log.date
    if log_date not in logs_by_date:
      logs_by_date[log_date] = []

    # Find the habit for this log
    habit = next((h for h in habits if h.id == log.habit_id), None)
    if habit:
      logs_by_date[log_date].append({
          'habit_id': str(log.habit_id),
          'habit_title': habit.title,
          'quantity': log.quantity,
          'target': habit.target,
          'logged_at': log.created_at
      })

  # Convert to the desired format
  day_logs = []
  total_logs = 0

  for date_key in sorted(logs_by_date.keys(), reverse=True):  # Most recent first
    habits_for_day = logs_by_date[date_key]
    day_logs.append(DayLogs(
        date=date_key,
        habits=[HabitLogEntry(**habit_data) for habit_data in habits_for_day],
        totalLogs=len(habits_for_day)
    ))
    total_logs += len(habits_for_day)

  return day_logs
  # OverviewResponse(
  #     logs=day_logs,
  #     total_days=len(day_logs),
  #     total_logs=total_logs
  # )


# @router.get("/daily-counts", response_model=list[DailyLogCount])
# def get_daily_log_counts(
#   days: int = Query(default=30, ge=1, le=365, description="Number of days to look back"),
#   db: Session = Depends(get_db),
#   current_user: User = Depends(verify_token)
# ):
#   """Get daily habit log counts for the user's habits over the specified number of days."""
#   end_date = date.today()
#   start_date = end_date - timedelta(days=days-1)

#   # Get all habits for the user
#   user_habits = db.query(Habit.id).filter(Habit.user_id == current_user.id).subquery()

#   # Query daily log counts
#   daily_counts = db.query(HabitLog.date, func.count(HabitLog.id).label('count')
#   ).join(
#       user_habits, HabitLog.habit_id == user_habits.c.id
#   ).filter(
#     and_(
#       HabitLog.date >= start_date,
#       HabitLog.date <= end_date
#     )
#   ).group_by(HabitLog.date).order_by(
#     HabitLog.date
#   ).all()

#   # Convert to dict for easier lookup
#   counts_dict = {row.date: row.count for row in daily_counts}

#   # Fill in missing dates with 0 counts
#   result = []
#   current_date = start_date
#   while current_date <= end_date:
#     count_value = counts_dict.get(current_date, 0)
#     # Ensure count is an integer
#     count = count_value if isinstance(count_value, int) else 0
#     result.append(DailyLogCount(date=current_date, count=count))
#     current_date += timedelta(days=1)

#   return result


@router.get("/{habit_id}/stats/streak", response_model=HabitStats)
def get_habit_stats_streak(
    habit_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
  """Get statistics for a specific habit using completion records."""
  habit = db.query(Habit).filter(Habit.id == uuid.UUID(
      habit_id), Habit.user_id == current_user.id).first()

  if not habit:
    raise HTTPException(status_code=404, detail="Habit not found")

  # Get streaks from completion records
  streak_data = get_habit_streak_from_completions(db, habit.id)
  current_streak = streak_data["current_streak"]
  longest_streak = streak_data["longest_streak"]

  # Get completion rate from completion records
  completion_stats = get_habit_completion_stats(db, habit.id)
  completion_rate = completion_stats["completion_rate"]

  return HabitStats(
      habit_id=str(habit.id),
      current_streak=current_streak,
      longest_streak=longest_streak,
      completion_rate=round(completion_rate, 2)
  )


@router.get("/{habit_id}/daily-progress", response_model=list[HabitDailyProgress])
def get_habit_daily_progress(
    habit_id: str,
    days: int = Query(default=7, ge=1, le=365,
                      description="Number of days to look back"),
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
  """Get daily progress for a specific habit over the specified number of days using completion records.
  Shows individual days for all habit types (original behavior).
  """
  habit = db.query(Habit).filter(Habit.id == uuid.UUID(
      habit_id), Habit.user_id == current_user.id).first()

  if not habit:
    raise HTTPException(status_code=404, detail="Habit not found")

  return _get_daily_progress(habit, days, db)

# use for individual habit chart


@router.get("/{habit_id}/progress", response_model=list[HabitDailyProgress])
def get_habit_progress(
    habit_id: str,
    periods: int = Query(default=7, ge=1, le=365,
                         description="Number of periods to look back"),
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
  """Get progress for a specific habit over the specified number of periods using completion records.
  For daily habits: shows days
  For weekly habits: shows weeks  
  For monthly habits: shows months
  """
  habit = db.query(Habit).filter(Habit.id == uuid.UUID(
      habit_id), Habit.user_id == current_user.id).first()

  if not habit:
    raise HTTPException(status_code=404, detail="Habit not found")

  if habit.frequency.value == "daily":
    return _get_daily_progress(habit, periods, db)
  elif habit.frequency.value == "weekly":
    return _get_weekly_progress(habit, periods, db)
  elif habit.frequency.value == "monthly":
    return _get_monthly_progress(habit, periods, db)
  else:
    # Fallback to daily for unknown frequencies
    return _get_daily_progress(habit, periods, db)


def _get_daily_progress(habit: Habit, days: int, db: Session) -> list[HabitDailyProgress]:
  """Get daily progress for daily habits."""
  end_date = date.today()
  start_date = end_date - timedelta(days=days-1)

  # Get completion records for this habit in the date range
  completions = db.query(HabitCompletion).filter(
      and_(
          HabitCompletion.habit_id == habit.id,
          HabitCompletion.date >= start_date,
          HabitCompletion.date <= end_date
      )
  ).all()

  # Convert to dict for faster lookup
  completion_dict = {comp.date: comp for comp in completions}

  # Generate progress data for each day
  result = []
  current_date = start_date
  while current_date <= end_date:
    if current_date in completion_dict:
      # Use completion record data
      completion = completion_dict[current_date]
      result.append(HabitDailyProgress(
          date=current_date,
          completed=completion.is_completed,
          target=completion.target_at_time,
          actual=completion.quantity_achieved,
          effective_target=completion.target_at_time
      ))
    else:
      # No completion record for this date
      result.append(HabitDailyProgress(
          date=current_date,
          completed=False,
          target=habit.target,
          actual=0,
          effective_target=habit.target
      ))
    current_date += timedelta(days=1)

  return result


def _get_weekly_progress(habit: Habit, weeks: int, db: Session) -> list[HabitDailyProgress]:
  """Get weekly progress for weekly habits."""
  today = date.today()

  # Get the Monday of the current week
  days_since_monday = today.weekday()
  current_week_start = today - timedelta(days=days_since_monday)

  # Generate progress data for each week
  result = []
  for i in range(weeks):
    week_start = current_week_start - timedelta(days=7 * i)
    week_end = week_start + timedelta(days=6)

    # Get completion records for this week
    completions = db.query(HabitCompletion).filter(
        and_(
            HabitCompletion.habit_id == habit.id,
            HabitCompletion.date >= week_start,
            HabitCompletion.date <= week_end
        )
    ).all()

    # Check if this week was completed
    is_completed = any(comp.is_completed for comp in completions)

    # Sum up quantities for this week
    total_quantity = sum(comp.quantity_achieved for comp in completions)

    # Use the most recent target (from the most recent completion record)
    target = habit.target
    if completions:
      target = completions[0].target_at_time

    result.append(HabitDailyProgress(
        date=week_start,  # Use Monday as the representative date
        completed=is_completed,
        target=target,
        actual=total_quantity,
        effective_target=target  # Target that was in effect during this week
    ))

  return result


def _get_monthly_progress(habit: Habit, months: int, db: Session) -> list[HabitDailyProgress]:
  """Get monthly progress for monthly habits."""
  today = date.today()

  # Generate progress data for each month
  result = []
  for i in range(months):
    # Calculate the month start date
    if today.month - i <= 0:
      month_start = today.replace(
          year=today.year - 1, month=12 + (today.month - i), day=1)
    else:
      month_start = today.replace(month=today.month - i, day=1)

    # Calculate the month end date
    if month_start.month == 12:
      month_end = month_start.replace(
          year=month_start.year + 1, month=1, day=1) - timedelta(days=1)
    else:
      month_end = month_start.replace(
          month=month_start.month + 1, day=1) - timedelta(days=1)

    # Get completion records for this month
    completions = db.query(HabitCompletion).filter(
        and_(
            HabitCompletion.habit_id == habit.id,
            HabitCompletion.date >= month_start,
            HabitCompletion.date <= month_end
        )
    ).all()

    # Check if this month was completed
    is_completed = any(comp.is_completed for comp in completions)

    # Sum up quantities for this month
    total_quantity = sum(comp.quantity_achieved for comp in completions)

    # Use the most recent target (from the most recent completion record)
    target = habit.target
    if completions:
      target = completions[0].target_at_time

    result.append(HabitDailyProgress(
        date=month_start,  # Use 1st of month as the representative date
        completed=is_completed,
        target=target,
        actual=total_quantity,
        effective_target=target  # Target that was in effect during this month
    ))

  return result


def get_week_start_end(today: date) -> tuple[date, date]:
  """Get the start and end dates of the week containing the given date."""
  # Get Monday of the current week
  days_since_monday = today.weekday()
  week_start = today - timedelta(days=days_since_monday)
  week_end = week_start + timedelta(days=6)
  return week_start, week_end


def get_month_start_end(today: date) -> tuple[date, date]:
  """Get the start and end dates of the month containing the given date."""
  month_start = today.replace(day=1)
  if today.month == 12:
    month_end = today.replace(
        year=today.year + 1, month=1, day=1) - timedelta(days=1)
  else:
    month_end = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
  return month_start, month_end


# Send today's habit logs stats
@router.get("/logs/today", response_model=list[TodayHabitLog])
def get_today_habits_logs_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
):
  """Get all user's habits with their completion status for the appropriate time period using completion records."""
  today = date.today()

  # Get all habits for the user
  habits = db.query(Habit).filter(Habit.user_id == current_user.id).all()

  if not habits:
    return []

  # Build response
  result = []
  for habit in habits:
    # Determine the time period based on habit frequency
    if habit.frequency.value == "daily":
      start_date = today
      end_date = today
    elif habit.frequency.value == "weekly":
      start_date, end_date = get_week_start_end(today)
    elif habit.frequency.value == "monthly":
      start_date, end_date = get_month_start_end(today)
    else:
      # Fallback to daily for unknown frequencies
      start_date = today
      end_date = today

    # Get completion records for the appropriate time period
    completions = db.query(HabitCompletion).filter(
        and_(
            HabitCompletion.habit_id == habit.id,
            HabitCompletion.date >= start_date,
            HabitCompletion.date <= end_date
        )
    ).all()

    # Sum quantities for current_progress
    current_progress = sum(comp.quantity_achieved for comp in completions)

    # Check if habit was completed in the appropriate period
    logged_today = any(comp.is_completed for comp in completions)

    # Get the most recent completion for log_id and log_created_at
    most_recent_completion = max(
        completions, key=lambda comp: comp.updated_at) if completions else None

    # Get the most recent log for log_id and log_created_at (fallback)
    if not most_recent_completion:
      period_logs = db.query(HabitLog).filter(
          and_(
              HabitLog.habit_id == habit.id,
              HabitLog.date >= start_date,
              HabitLog.date <= end_date
          )
      ).all()
      most_recent_log = max(
          period_logs, key=lambda log: log.created_at) if period_logs else None
    else:
      most_recent_log = None

    result.append(TodayHabitLog(
        habit_id=str(habit.id),
        title=habit.title,
        category=habit.category.value,
        frequency=habit.frequency.value,
        target=habit.target,
        logged_today=logged_today,
        current_progress=current_progress,
        log_id=str(most_recent_completion.id) if most_recent_completion else (
            str(most_recent_log.id) if most_recent_log else None),
        log_created_at=most_recent_completion.updated_at if most_recent_completion else (
            most_recent_log.created_at if most_recent_log else None)
    ))

  return result
