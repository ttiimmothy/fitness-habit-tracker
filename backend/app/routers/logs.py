from uuid import UUID
from datetime import date, datetime, timedelta
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_limiter.depends import RateLimiter
from app.core.config import settings
from sqlalchemy import func, and_, desc
from sqlalchemy.orm import Session

from app.middleware.verify_token import verify_token
from app.db.session import get_db
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.models.user import User
from app.schemas.habit_log import HabitLogCreate, HabitLogOut
from app.schemas.stats import TodayHabitLog
from app.services.completion_service import update_habit_completion


router = APIRouter()


@router.post("/{habit_id}/log", response_model=HabitLogOut)
def create_log(habit_id: str, payload: HabitLogCreate, db: Session = Depends(get_db), current_user: User = Depends(verify_token)):
  habit = db.query(Habit).filter(Habit.id == UUID(
      habit_id), Habit.user_id == current_user.id).first()

  if not habit:
    raise HTTPException(status_code=404, detail="Habit not found")

  log_date = payload.date or date.today()
  existing = db.query(HabitLog).filter(HabitLog.habit_id ==
                                       habit.id, HabitLog.date == log_date).first()

  # Calculate total quantity after adding new quantity
  current_quantity = existing.quantity if existing else 0
  new_total_quantity = current_quantity + payload.quantity

  # Check if new total would exceed the habit's target
  if new_total_quantity > habit.target:
    remaining = habit.target - current_quantity
    if remaining <= 0:
      raise HTTPException(
          status_code=400, detail=f"Habit target already reached for {log_date}. Target: {habit.target}, Current: {current_quantity}")
    else:
      raise HTTPException(
          status_code=400, detail=f"Quantity would exceed habit target. Target: {habit.target}, Current: {current_quantity}, Requested: {payload.quantity}, Remaining: {remaining}")

  if existing:
    # Update existing log by adding quantity
    existing.quantity += payload.quantity
    db.commit()
    db.refresh(existing)

    # Update completion status for this date
    update_habit_completion(db, habit.id, log_date)
    db.commit()

    return HabitLogOut(**{
        "id": str(existing.id),
        "habit_id": str(existing.habit_id),
        "date": existing.date,
        "quantity": existing.quantity,
        "created_at": existing.created_at
    })
  else:
    # Create new log with quantity
    log = HabitLog(habit_id=habit.id, date=log_date, quantity=payload.quantity)
    db.add(log)
    db.commit()
    db.refresh(log)

    # Update completion status for this date
    update_habit_completion(db, habit.id, log_date)
    db.commit()

    return HabitLogOut(**{
        "id": str(log.id),
        "habit_id": str(log.habit_id),
        "date": log.date,
        "quantity": log.quantity,
        "created_at": log.created_at
    })


@router.get("/", response_model=list[HabitLogOut])
def list_logs(habit_id: str = Query(..., description="Habit ID"), date: date | None = Query(default=None, description="Filter by date"), db: Session = Depends(get_db), current_user: User = Depends(verify_token)):
  habit = db.query(Habit).filter(Habit.id == UUID(habit_id),
                                 Habit.user_id == current_user.id).first()

  if not habit:
    raise HTTPException(status_code=404, detail="Habit not found")

  q = db.query(HabitLog).filter(HabitLog.habit_id == habit.id)

  if date:
    q = q.filter(HabitLog.date == date)

  q = q.order_by(HabitLog.date.desc())
  logs = q.all()

  return [HabitLogOut(**{"id": str(l.id), "habit_id": str(l.habit_id), "date": l.date, "quantity": l.quantity, "created_at": l.created_at}) for l in logs]
