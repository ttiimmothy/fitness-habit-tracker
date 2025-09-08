import uuid
from datetime import date
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from app.api.dependencies.get_current_user import get_current_user
from app.db.session import get_db
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.models.user import User
from app.schemas.common import HabitLogCreate, HabitLogOut


router = APIRouter()


@router.post("/{habit_id}/log", response_model=HabitLogOut, dependencies=[Depends(RateLimiter(times=60, seconds=3600))])
def create_log(habit_id: str, payload: HabitLogCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  habit = db.query(Habit).filter(Habit.id == uuid.UUID(habit_id), Habit.user_id == current_user.id).first()
  
  if not habit:
    raise HTTPException(status_code=404, detail="Habit not found")
  log_date = payload.date or date.today()
  existing = db.query(HabitLog).filter(HabitLog.habit_id == habit.id, HabitLog.date == log_date).first()
  
  if existing:
    raise HTTPException(status_code=409, detail="Log for date already exists")
  
  log = HabitLog(habit_id=habit.id, date=log_date)
  
  db.add(log)
  db.commit()
  db.refresh(log)
  
  return HabitLogOut(**{"id": str(log.id), "habit_id": str(log.habit_id), "date": log.date, "created_at": log.created_at})


@router.get("/{habit_id}/logs", response_model=list[HabitLogOut])
def list_logs(habit_id: str, range: Literal["week", "month"] | None = Query(default=None), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  habit = db.query(Habit).filter(Habit.id == uuid.UUID(habit_id), Habit.user_id == current_user.id).first()
  
  if not habit:
    raise HTTPException(status_code=404, detail="Habit not found")
  
  q = db.query(HabitLog).filter(HabitLog.habit_id == habit.id).order_by(HabitLog.date.desc())
  logs = q.all()
  
  return [HabitLogOut(**{"id": str(l.id), "habit_id": str(l.habit_id), "date": l.date, "created_at": l.created_at}) for l in logs]
