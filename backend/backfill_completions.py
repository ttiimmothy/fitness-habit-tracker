#!/usr/bin/env python3
"""
Backfill script to populate habit_completions table with historical data.
This script calculates completion status for all existing habit logs.
"""

import sys
from datetime import date, datetime
from collections import defaultdict
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.models.habit_completion import HabitCompletion


def backfill_habit_completions(db: Session, habit_id: str = None) -> None:
  """
  Backfill habit_completions table with historical data.

  Args:
      db: Database session
      habit_id: Optional specific habit ID to backfill. If None, backfills all habits.
  """
  print("🔄 Starting habit completions backfill...")

  # Get habits to process
  if habit_id:
    habits = db.query(Habit).filter(Habit.id == habit_id).all()
    if not habits:
      print(f"❌ Habit with ID {habit_id} not found")
      return
  else:
    habits = db.query(Habit).all()

  print(f"📊 Found {len(habits)} habits to process")

  total_completions_created = 0

  for habit in habits:
    print(f"\n📝 Processing habit: {habit.title} (ID: {habit.id})")

    # Get all logs for this habit
    logs = db.query(HabitLog).filter(
        HabitLog.habit_id == habit.id
    ).order_by(HabitLog.date).all()

    if not logs:
      print(f"  ⚠️  No logs found for habit '{habit.title}'")
      continue

    # Group logs by date and sum quantities
    daily_totals = defaultdict(int)
    for log in logs:
      daily_totals[log.date] += log.quantity

    print(f"  📅 Found logs for {len(daily_totals)} unique dates")

    # Create completion records
    completions_created = 0
    for log_date, total_quantity in daily_totals.items():
      # Check if completion record already exists
      existing = db.query(HabitCompletion).filter(
          HabitCompletion.habit_id == habit.id,
          HabitCompletion.date == log_date
      ).first()

      if existing:
        print(f"  ⚠️  Completion record already exists for {log_date}")
        continue

      # Determine if habit was completed on this date
      is_completed = total_quantity >= habit.target

      # Create completion record
      completion = HabitCompletion(
          habit_id=habit.id,
          date=log_date,
          is_completed=is_completed,
          target_at_time=habit.target,
          quantity_achieved=total_quantity
      )

      db.add(completion)
      completions_created += 1

      status = "✅" if is_completed else "❌"
      print(f"    {status} {log_date}: {total_quantity}/{habit.target} ({'completed' if is_completed else 'incomplete'})")

    # Commit completions for this habit
    try:
      db.commit()
      print(
          f"  ✅ Created {completions_created} completion records for '{habit.title}'")
      total_completions_created += completions_created
    except Exception as e:
      print(f"  ❌ Error creating completions for '{habit.title}': {e}")
      db.rollback()

  print(
      f"\n🎉 Backfill completed! Created {total_completions_created} total completion records")


def main():
  """Main function to run the backfill script."""
  print("🚀 Habit Completions Backfill Script")
  print("=" * 50)

  # Get database session
  db = next(get_db())

  try:
    # Check if habit_id provided as command line argument
    habit_id = sys.argv[1] if len(sys.argv) > 1 else None

    if habit_id:
      print(f"🎯 Backfilling specific habit: {habit_id}")
    else:
      print("🌍 Backfilling all habits")

    # Run backfill
    backfill_habit_completions(db, habit_id)

  except Exception as e:
    print(f"❌ Error during backfill: {e}")
    db.rollback()
    sys.exit(1)
  finally:
    db.close()

  print("\n✨ Backfill script completed successfully!")


if __name__ == "__main__":
  main()
