"""Service functions for managing habit completions."""

import uuid
from datetime import date, datetime, timezone, timedelta, UTC
from collections import defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.models.habit_completion import HabitCompletion


def update_habit_completion(db: Session, habit_id: uuid.UUID, completion_date: date) -> HabitCompletion:
  """
  Update or create a habit completion record for a specific date.
  For weekly/monthly habits, checks if the period total meets the target.
  Uses stored target_at_time for historical accuracy when available.

  Args:
      db: Database session
      habit_id: ID of the habit
      completion_date: Date to update completion for

  Returns:
      HabitCompletion: The updated or created completion record
  """
  # Get the habit
  habit = db.query(Habit).filter(Habit.id == habit_id).first()
  if not habit:
    raise ValueError(f"Habit with ID {habit_id} not found")

  # Determine the period based on habit frequency
  if habit.frequency.value == "daily":
    # For daily habits: check if this day meets the target
    period_start = completion_date
    period_end = completion_date
  elif habit.frequency.value == "weekly":
    # For weekly habits: check if the week meets the target
    days_since_monday = completion_date.weekday()
    period_start = completion_date - timedelta(days=days_since_monday)
    period_end = period_start + timedelta(days=6)
  elif habit.frequency.value == "monthly":
    # For monthly habits: check if the month meets the target
    period_start = completion_date.replace(day=1)
    if completion_date.month == 12:
      period_end = completion_date.replace(
          year=completion_date.year + 1, month=1, day=1) - timedelta(days=1)
    else:
      period_end = completion_date.replace(
          month=completion_date.month + 1, day=1) - timedelta(days=1)
  else:
    # Fallback to daily for unknown frequencies
    period_start = completion_date
    period_end = completion_date

  # Get all logs for this habit in the period
  period_logs = db.query(HabitLog).filter(
      and_(
          HabitLog.habit_id == habit_id,
          HabitLog.date >= period_start,
          HabitLog.date <= period_end
      )
  ).all()

  # Calculate total quantity for the period (for completion check)
  period_total_quantity = sum(log.quantity for log in period_logs)

  # Get logs for this specific date (for quantity_achieved)
  daily_logs = db.query(HabitLog).filter(
      and_(
          HabitLog.habit_id == habit_id,
          HabitLog.date == completion_date
      )
  ).all()

  # Calculate quantity for this specific date
  daily_quantity = sum(log.quantity for log in daily_logs)

  # Check if completion record already exists
  existing_completion = db.query(HabitCompletion).filter(
      and_(
          HabitCompletion.habit_id == habit_id,
          HabitCompletion.date == completion_date
      )
  ).first()

  if existing_completion:
    # Update existing record using stored target for historical accuracy
    stored_target = existing_completion.target_at_time
    is_completed = period_total_quantity >= stored_target

    existing_completion.is_completed = is_completed
    existing_completion.quantity_achieved = daily_quantity
    existing_completion.updated_at = datetime.now(UTC)
    return existing_completion
  else:
    # Create new record with current target
    is_completed = period_total_quantity >= habit.target
    completion = HabitCompletion(
        habit_id=habit_id,
        date=completion_date,
        is_completed=is_completed,
        target_at_time=habit.target,
        quantity_achieved=daily_quantity
    )
    db.add(completion)
    return completion


def recalculate_habit_completions(db: Session, habit_id: uuid.UUID) -> int:
  """
  Recalculate all completion records for a habit (useful when target changes).
  For weekly/monthly habits, checks if the period total meets the target.
  Uses the stored target_at_time values to preserve historical accuracy.

  Args:
      db: Database session
      habit_id: ID of the habit to recalculate

  Returns:
      int: Number of completion records updated
  """
  # Get the habit
  habit = db.query(Habit).filter(Habit.id == habit_id).first()
  if not habit:
    raise ValueError(f"Habit with ID {habit_id} not found")

  # Get all existing completion records for this habit
  completions = db.query(HabitCompletion).filter(
      HabitCompletion.habit_id == habit_id
  ).all()

  updated_count = 0

  for completion in completions:
    # Determine the period based on habit frequency
    if habit.frequency.value == "daily":
      # For daily habits: check if this day meets the target
      period_start = completion.date
      period_end = completion.date
    elif habit.frequency.value == "weekly":
      # For weekly habits: check if the week meets the target
      days_since_monday = completion.date.weekday()
      period_start = completion.date - timedelta(days=days_since_monday)
      period_end = period_start + timedelta(days=6)
    elif habit.frequency.value == "monthly":
      # For monthly habits: check if the month meets the target
      period_start = completion.date.replace(day=1)
      if completion.date.month == 12:
        period_end = completion.date.replace(
            year=completion.date.year + 1, month=1, day=1) - timedelta(days=1)
      else:
        period_end = completion.date.replace(
            month=completion.date.month + 1, day=1) - timedelta(days=1)
    else:
      # Fallback to daily for unknown frequencies
      period_start = completion.date
      period_end = completion.date

    # Get all logs for this habit in the period
    period_logs = db.query(HabitLog).filter(
        and_(
            HabitLog.habit_id == habit_id,
            HabitLog.date >= period_start,
            HabitLog.date <= period_end
        )
    ).all()

    # Calculate total quantity for the period (for completion check)
    period_total_quantity = sum(log.quantity for log in period_logs)

    # Get logs for this specific date (for quantity_achieved)
    daily_logs = db.query(HabitLog).filter(
        and_(
            HabitLog.habit_id == habit_id,
            HabitLog.date == completion.date
        )
    ).all()

    # Calculate quantity for this specific date
    daily_quantity = sum(log.quantity for log in daily_logs)

    # Use the stored target_at_time for historical accuracy
    stored_target = completion.target_at_time
    is_completed = period_total_quantity >= stored_target

    # Update completion record using stored target
    completion.is_completed = is_completed
    completion.quantity_achieved = daily_quantity
    completion.updated_at = datetime.now(UTC)

    updated_count += 1

  return updated_count


def update_habit_completions_for_new_target(db: Session, habit_id: uuid.UUID, new_target: int) -> int:
  """
  Update completion records for a habit when the target changes.
  Only updates records that don't have logs yet (future dates) or recent records.
  Preserves historical accuracy by keeping old target_at_time values.

  Args:
      db: Database session
      habit_id: ID of the habit
      new_target: The new target value

  Returns:
      int: Number of completion records updated
  """
  # Get the habit
  habit = db.query(Habit).filter(Habit.id == habit_id).first()
  if not habit:
    raise ValueError(f"Habit with ID {habit_id} not found")

  # Get all completion records for this habit
  completions = db.query(HabitCompletion).filter(
      HabitCompletion.habit_id == habit_id
  ).all()

  updated_count = 0
  today = date.today()

  for completion in completions:
    # Only update completions for today or future dates
    # This preserves historical accuracy for past dates
    if completion.date >= today:
      # Get all logs for this specific date
      logs = db.query(HabitLog).filter(
          and_(
              HabitLog.habit_id == habit_id,
              HabitLog.date == completion.date
          )
      ).all()

      total_quantity = sum(log.quantity for log in logs)
      is_completed = total_quantity >= new_target

      # Update completion record with new target
      completion.is_completed = is_completed
      completion.target_at_time = new_target
      completion.quantity_achieved = total_quantity
      completion.updated_at = datetime.now(UTC)

      updated_count += 1

  return updated_count


def get_habit_completion_stats(db: Session, habit_id: uuid.UUID, start_date: date | None = None, end_date: date | None = None) -> dict:
  """
  Get completion statistics for a habit within a date range.
  Handles daily, weekly, and monthly habits correctly.

  Args:
      db: Database session
      habit_id: ID of the habit
      start_date: Start date for statistics (inclusive)
      end_date: End date for statistics (inclusive)

  Returns:
      dict: Statistics including total periods, completed periods, completion rate
  """
  # Get the habit to determine frequency
  habit = db.query(Habit).filter(Habit.id == habit_id).first()
  if not habit:
    return {
        "total_days": 0,
        "completed_days": 0,
        "completion_rate": 0.0
    }

  # Build query
  query = db.query(HabitCompletion).filter(
      HabitCompletion.habit_id == habit_id)

  if start_date:
    query = query.filter(HabitCompletion.date >= start_date)
  if end_date:
    query = query.filter(HabitCompletion.date <= end_date)

  completions = query.all()

  if not completions:
    return {
        "total_days": 0,
        "completed_days": 0,
        "completion_rate": 0.0
    }

  if habit.frequency.value == "daily":
    return _calculate_daily_completion_stats(completions)
  elif habit.frequency.value == "weekly":
    return _calculate_weekly_completion_stats(completions, habit)
  elif habit.frequency.value == "monthly":
    return _calculate_monthly_completion_stats(completions, habit)
  else:
    # Fallback to daily for unknown frequencies
    return _calculate_daily_completion_stats(completions)


def _calculate_daily_completion_stats(completions: list) -> dict:
  """Calculate completion stats for daily habits."""
  total_days = len(completions)
  completed_days = sum(1 for c in completions if c.is_completed)
  completion_rate = (completed_days / total_days) * \
      100 if total_days > 0 else 0.0

  return {
      "total_days": total_days,
      "completed_days": completed_days,
      "completion_rate": completion_rate
  }


def _calculate_weekly_completion_stats(completions: list, habit) -> dict:
  """Calculate completion stats for weekly habits."""
  # Group completions by calendar week
  weekly_completions = {}
  for completion in completions:
    # Get Monday of the week containing this date
    days_since_monday = completion.date.weekday()
    week_start = completion.date - timedelta(days=days_since_monday)

    if week_start not in weekly_completions:
      weekly_completions[week_start] = []
    weekly_completions[week_start].append(completion)

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
  total_weeks = ((current_week_start - creation_week_start).days // 7) + 1

  # Count weeks with at least one successful completion
  successful_weeks = 0
  for _week_start, week_completions in weekly_completions.items():
    if any(comp.is_completed for comp in week_completions):
      successful_weeks += 1

  completion_rate = (successful_weeks / total_weeks) * \
      100 if total_weeks > 0 else 0.0

  return {
      "total_days": total_weeks,  # Using total_days for consistency with API
      "completed_days": successful_weeks,
      "completion_rate": completion_rate
  }


def _calculate_monthly_completion_stats(completions: list, habit) -> dict:
  """Calculate completion stats for monthly habits."""
  # Group completions by month
  monthly_completions = {}
  for completion in completions:
    month_start = completion.date.replace(day=1)

    if month_start not in monthly_completions:
      monthly_completions[month_start] = []
    monthly_completions[month_start].append(completion)

  # Calculate total months since habit creation
  habit_creation = habit.created_at.date()
  today = date.today()

  # Calculate total months (inclusive)
  total_months = ((today.year - habit_creation.year) * 12 +
                  (today.month - habit_creation.month)) + 1

  # Count months with at least one successful completion
  successful_months = 0
  for _month_start, month_completions in monthly_completions.items():
    if any(comp.is_completed for comp in month_completions):
      successful_months += 1

  completion_rate = (successful_months / total_months) * \
      100 if total_months > 0 else 0.0

  return {
      "total_days": total_months,  # Using total_days for consistency with API
      "completed_days": successful_months,
      "completion_rate": completion_rate
  }


def get_habit_streak_from_completions(db: Session, habit_id: uuid.UUID) -> dict:
  """
  Calculate current and longest streaks using completion records.
  Handles daily, weekly, and monthly habits correctly.

  Args:
      db: Database session
      habit_id: ID of the habit

  Returns:
      dict: Current streak and longest streak
  """
  # Get the habit to determine frequency
  habit = db.query(Habit).filter(Habit.id == habit_id).first()
  if not habit:
    return {"current_streak": 0, "longest_streak": 0}

  # Get all completion records for this habit, ordered by date desc
  completions = db.query(HabitCompletion).filter(
      HabitCompletion.habit_id == habit_id
  ).order_by(HabitCompletion.date.desc()).all()

  if not completions:
    return {"current_streak": 0, "longest_streak": 0}

  # Get successful dates (completed days)
  successful_dates = [c.date for c in completions if c.is_completed]

  if not successful_dates:
    return {"current_streak": 0, "longest_streak": 0}

  # Sort successful dates in descending order
  successful_dates.sort(reverse=True)

  if habit.frequency.value == "daily":
    return _calculate_daily_streaks(successful_dates)
  elif habit.frequency.value == "weekly":
    return _calculate_weekly_streaks(successful_dates)
  elif habit.frequency.value == "monthly":
    return _calculate_monthly_streaks(successful_dates)
  else:
    # Fallback to daily for unknown frequencies
    return _calculate_daily_streaks(successful_dates)


def _calculate_daily_streaks(successful_dates: list[date]) -> dict:
  """Calculate streaks for daily habits."""
  current_streak = 0
  if successful_dates:
    # Check if today or yesterday was completed
    today = date.today()
    yesterday = today - timedelta(days=1)

    if successful_dates[0] == today or successful_dates[0] == yesterday:
      current_streak = 1
      # Count consecutive days from the most recent
      for i in range(1, len(successful_dates)):
        if (successful_dates[i-1] - successful_dates[i]).days == 1:
          current_streak += 1
        else:
          break

  # Calculate longest streak
  longest_streak = 0
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
    longest_streak = 1 if successful_dates else 0

  return {
      "current_streak": current_streak,
      "longest_streak": longest_streak
  }


def _calculate_weekly_streaks(successful_dates: list[date]) -> dict:
  """Calculate streaks for weekly habits."""
  # Group successful dates by calendar week (Monday-Sunday)
  successful_weeks = set()
  for log_date in successful_dates:
    # Get Monday of the week containing this date
    days_since_monday = log_date.weekday()
    week_start = log_date - timedelta(days=days_since_monday)
    successful_weeks.add(week_start)

  successful_weeks = sorted(successful_weeks, reverse=True)

  if not successful_weeks:
    return {"current_streak": 0, "longest_streak": 0}

  # Calculate current streak (consecutive weeks from current week backwards)
  today = date.today()
  days_since_monday = today.weekday()
  current_week_start = today - timedelta(days=days_since_monday)
  current_week = current_week_start

  current_streak = 0
  for week_start in successful_weeks:
    if week_start == current_week:
      current_streak += 1
      current_week -= timedelta(days=7)  # Go back one week
    elif week_start < current_week:
      break

  # Calculate longest streak
  longest_streak = 0
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
    longest_streak = 1 if successful_weeks else 0

  return {
      "current_streak": current_streak,
      "longest_streak": longest_streak
  }


def _calculate_monthly_streaks(successful_dates: list[date]) -> dict:
  """Calculate streaks for monthly habits."""
  # Group successful dates by month
  successful_months = set()
  for log_date in successful_dates:
    month_start = log_date.replace(day=1)
    successful_months.add(month_start)

  successful_months = sorted(successful_months, reverse=True)

  if not successful_months:
    return {"current_streak": 0, "longest_streak": 0}

  # Calculate current streak (consecutive months from current month backwards)
  today = date.today()
  current_month_start = today.replace(day=1)
  current_month = current_month_start

  current_streak = 0
  for month_start in successful_months:
    if month_start == current_month:
      current_streak += 1
      # Go back one month
      if current_month.month == 1:
        current_month = current_month.replace(
            year=current_month.year - 1, month=12)
      else:
        current_month = current_month.replace(month=current_month.month - 1)
    elif month_start < current_month:
      break

  # Calculate longest streak
  longest_streak = 0
  if len(successful_months) > 1:
    temp_streak = 1
    for i in range(1, len(successful_months)):
      # Check if months are consecutive
      prev_month = successful_months[i-1]
      curr_month = successful_months[i]

      # Calculate if they are consecutive months
      if prev_month.month == 1:
        expected_prev = curr_month.replace(year=curr_month.year + 1, month=12)
      else:
        expected_prev = curr_month.replace(month=curr_month.month + 1)

      if prev_month == expected_prev:
        temp_streak += 1
      else:
        longest_streak = max(longest_streak, temp_streak)
        temp_streak = 1
    longest_streak = max(longest_streak, temp_streak)
  else:
    longest_streak = 1 if successful_months else 0

  return {
      "current_streak": current_streak,
      "longest_streak": longest_streak
  }
