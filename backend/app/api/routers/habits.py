import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.get_current_user import get_current_user
from app.db.session import get_db
from app.models.habit import Habit, Frequency
from app.models.user import User
from app.schemas.common import HabitOut, HabitCreate, HabitUpdate


router = APIRouter()


@router.get("", response_model=list[HabitOut])
def list_habits(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  habits = db.query(Habit).filter(Habit.user_id == current_user.id).order_by(Habit.created_at.desc()).all()
  return [HabitOut(**{
    "id": str(h.id),
    "user_id": str(h.user_id),
    "title": h.title,
    "frequency": h.frequency.value,
    "target": h.target,
    "created_at": h.created_at,
  }) for h in habits]


@router.post("", response_model=HabitOut, status_code=201)
def create_habit(payload: HabitCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  try:
    freq = Frequency(payload.frequency)
  except ValueError:
    raise HTTPException(status_code=422, detail="Invalid frequency")
  habit = Habit(user_id=current_user.id, title=payload.title, frequency=freq, target=payload.target)
  db.add(habit)
  db.commit()
  db.refresh(habit)
  return HabitOut(**{
    "id": str(habit.id),
    "user_id": str(habit.user_id),
    "title": habit.title,
    "frequency": habit.frequency.value,
    "target": habit.target,
    "created_at": habit.created_at,
  })


@router.get("/{habit_id}", response_model=HabitOut)
def get_habit(habit_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  habit = db.query(Habit).filter(Habit.id == uuid.UUID(habit_id), Habit.user_id == current_user.id).first()
  if not habit:
    raise HTTPException(status_code=404, detail="Habit not found")
  return HabitOut(**{
    "id": str(habit.id),
    "user_id": str(habit.user_id),
    "title": habit.title,
    "frequency": habit.frequency.value,
    "target": habit.target,
    "created_at": habit.created_at,
  })


@router.put("/{habit_id}", response_model=HabitOut)
def update_habit(habit_id: str, payload: HabitUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  habit = db.query(Habit).filter(Habit.id == uuid.UUID(habit_id), Habit.user_id == current_user.id).first()
  if not habit:
    raise HTTPException(status_code=404, detail="Habit not found")
  if payload.title is not None:
    habit.title = payload.title
  if payload.frequency is not None:
    try:
      habit.frequency = Frequency(payload.frequency)
    except ValueError:
      raise HTTPException(status_code=422, detail="Invalid frequency")
  if payload.target is not None:
    habit.target = payload.target
  db.commit()
  db.refresh(habit)
  return HabitOut(**{
    "id": str(habit.id),
    "user_id": str(habit.user_id),
    "title": habit.title,
    "frequency": habit.frequency.value,
    "target": habit.target,
    "created_at": habit.created_at,
  })


@router.delete("/{habit_id}", status_code=204)
def delete_habit(habit_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  habit = db.query(Habit).filter(Habit.id == uuid.UUID(habit_id), Habit.user_id == current_user.id).first()
  if not habit:
    raise HTTPException(status_code=404, detail="Habit not found")
  db.delete(habit)
  db.commit()
  return None
