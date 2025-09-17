import uuid
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc

from app.middleware.verify_token import verify_token
from app.db.session import get_db
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.models.user import User
from app.schemas.stats import TodayHabitLog, DailyLogCount, HabitStats, HabitDailyProgress, OverviewResponse, DayLogs, HabitLogEntry

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

  # Group logs by date and sum quantities to check if target is met
  daily_totals = {}
  for log in logs:
    if log.date not in daily_totals:
      daily_totals[log.date] = 0
    daily_totals[log.date] += log.quantity

  # Filter successful completions based on habit frequency
  if habit.frequency.value == "daily":
    # For daily habits: check if each day meets the target
    successful_dates = [date for date,
                        total in daily_totals.items() if total >= habit.target]
  elif habit.frequency.value == "weekly":
    # For weekly habits: group by week and check if weekly total meets target
    weekly_totals = {}
    for log_date, total in daily_totals.items():
      # Get Monday of the week containing this date
      days_since_monday = log_date.weekday()
      week_start = log_date - timedelta(days=days_since_monday)
      if week_start not in weekly_totals:
        weekly_totals[week_start] = 0
      weekly_totals[week_start] += total

    # Find weeks that meet the target
    successful_weeks = [week_start for week_start,
                        total in weekly_totals.items() if total >= habit.target]

    # Convert back to successful dates (all dates in successful weeks)
    successful_dates = []
    for week_start in successful_weeks:
      for log_date, total in daily_totals.items():
        days_since_monday = log_date.weekday()
        week_start_for_date = log_date - timedelta(days=days_since_monday)
        if week_start_for_date == week_start:
          successful_dates.append(log_date)
  else:  # monthly
    # For monthly habits: group by month and check if monthly total meets target
    monthly_totals = {}
    for log_date, total in daily_totals.items():
      month_start = log_date.replace(day=1)
      if month_start not in monthly_totals:
        monthly_totals[month_start] = 0
      monthly_totals[month_start] += total

    # Find months that meet the target
    successful_months = [month_start for month_start,
                         total in monthly_totals.items() if total >= habit.target]

    # Convert back to successful dates (all dates in successful months)
    successful_dates = []
    for month_start in successful_months:
      for log_date, total in daily_totals.items():
        month_start_for_date = log_date.replace(day=1)
        if month_start_for_date == month_start:
          successful_dates.append(log_date)

  # Calculate streaks based on successful completions
  current_streak = 0
  longest_streak = 0

  if habit.frequency.value == "daily":
    # Daily habits: consecutive days
    if successful_dates:
      today = date.today()
      current_date = today

      # Calculate current streak (consecutive days from today backwards)
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

  elif habit.frequency.value == "weekly":
    # Weekly habits: consecutive weeks (using calendar weeks)
    if successful_dates:
      # Group successful dates by calendar week (Monday-Sunday)
      successful_weeks = set()
      for log_date in successful_dates:
        # Get Monday of the week containing this date
        days_since_monday = log_date.weekday()
        week_start = log_date - timedelta(days=days_since_monday)
        successful_weeks.add(week_start)

      successful_weeks = sorted(successful_weeks, reverse=True)

      # Calculate current streak (consecutive weeks from current week backwards)
      today = date.today()
      days_since_monday = today.weekday()
      current_week_start = today - timedelta(days=days_since_monday)
      current_week = current_week_start

      for week_start in successful_weeks:
        if week_start == current_week:
          current_streak += 1
          current_week -= timedelta(days=7)  # Go back one week
        elif week_start < current_week:
          break

      # Calculate longest streak
      if len(successful_weeks) > 1:
        temp_streak = 1
        for i in range(1, len(successful_weeks)):
          if (successful_weeks[i-1] - successful_weeks[i]).days == 7:
            temp_streak += 1
          else:
            longest_streak = max(longest_streak, temp_streak)
            temp_streak = 1
        longest_streak = max(longest_streak, temp_streak)
      else:
        longest_streak = 1

  else:  # monthly
    # Monthly habits: consecutive months
    if successful_dates:
      # Group successful dates by month
      successful_months = set()
      for log_date in successful_dates:
        days_since_creation = (log_date - habit.created_at.date()).days
        month_number = days_since_creation // 30
        successful_months.add(month_number)

      successful_months = sorted(successful_months, reverse=True)

      # Calculate current streak (consecutive months from current month backwards)
      current_month = (date.today() - habit.created_at.date()).days // 30
      current_month_num = current_month

      for month_num in successful_months:
        if month_num == current_month_num:
          current_streak += 1
          current_month_num -= 1
        elif month_num < current_month_num:
          break

      # Calculate longest streak
      if len(successful_months) > 1:
        temp_streak = 1
        for i in range(1, len(successful_months)):
          if successful_months[i-1] - successful_months[i] == 1:
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
    # For weekly habits: count calendar weeks with at least one successful completion
    # Calculate total weeks since habit creation
    habit_creation = habit.created_at.date()
    today = date.today()

    # Get the Monday of the week when habit was created
    days_since_monday_creation = habit_creation.weekday()
    creation_week_start = habit_creation - \
        timedelta(days=days_since_monday_creation)

    # Get the Monday of the current week
    days_since_monday_today = today.weekday()
    current_week_start = today - timedelta(days=days_since_monday_today)

    # Calculate total weeks (inclusive)
    weeks_since_creation = (
        (current_week_start - creation_week_start).days // 7) + 1

    # Group successful dates by calendar week and count weeks with at least one success
    successful_weeks = set()
    for log_date in successful_dates:
      # Get Monday of the week containing this date
      days_since_monday = log_date.weekday()
      week_start = log_date - timedelta(days=days_since_monday)
      successful_weeks.add(week_start)

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

# use for individual habit chart


@router.get("/{habit_id}/daily-progress", response_model=list[HabitDailyProgress])
def get_habit_daily_progress(
    habit_id: str,
    days: int = Query(default=7, ge=1, le=365,
                      description="Number of days to look back"),
    db: Session = Depends(get_db),
    current_user: User = Depends(verify_token)
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
  """Get all user's habits with their completion status for the appropriate time period."""
  today = date.today()

  # Get all habits for the user
  habits = db.query(Habit).filter(Habit.user_id == current_user.id).all()

  if not habits:
    return []

  # Get all habit IDs
  habit_ids = [habit.id for habit in habits]

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

    # Get logs for the appropriate time period
    period_logs = db.query(HabitLog).filter(
        and_(
            HabitLog.habit_id == habit.id,
            HabitLog.date >= start_date,
            HabitLog.date <= end_date
        )
    ).all()

    # Sum quantities for current_progress
    current_progress = sum(log.quantity for log in period_logs)

    # Check if habit was completed (logged) in the appropriate period
    logged_today = current_progress > 0

    # Get the most recent log for log_id and log_created_at
    most_recent_log = max(
        period_logs, key=lambda log: log.created_at) if period_logs else None

    result.append(TodayHabitLog(
        habit_id=str(habit.id),
        title=habit.title,
        category=habit.category.value,
        frequency=habit.frequency.value,
        target=habit.target,
        logged_today=logged_today,
        current_progress=current_progress,
        log_id=str(most_recent_log.id) if most_recent_log else None,
        log_created_at=most_recent_log.created_at if most_recent_log else None
    ))

  return result
