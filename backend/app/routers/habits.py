from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session

from app.api.middleware.get_current_user import get_current_user
from app.db.session import get_db
from app.models.habit import Habit, Frequency, Category
from app.models.user import User
from app.schemas.habit import HabitOut, HabitCreate, HabitUpdate


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
    "category": h.category.value,
    "description": h.description,
    "created_at": h.created_at,
  }) for h in habits]


@router.post("", response_model=HabitOut, status_code=201)
def create_habit(payload: HabitCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  try:
    freq = Frequency(payload.frequency)
  except ValueError:
    raise HTTPException(status_code=422, detail="Invalid frequency")

  try:
    category = Category(payload.category)
  except ValueError:
    raise HTTPException(status_code=422, detail="Invalid category")

  habit = Habit(user_id=current_user.id, title=payload.title, frequency=freq, target=payload.target, category=category, description=payload.description)
  db.add(habit)
  db.commit()
  db.refresh(habit)
  return HabitOut(**{
    "id": str(habit.id),
    "user_id": str(habit.user_id),
    "title": habit.title,
    "frequency": habit.frequency.value,
    "target": habit.target,
    "category": habit.category.value,
    "description": habit.description,
    "created_at": habit.created_at,
  })


@router.get("/{habit_id}", response_model=HabitOut)
def get_habit(
        habit_id: UUID = Path(..., description="Habit ID (UUID)"), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  habit = db.query(Habit).filter(Habit.id == habit_id,
                                 Habit.user_id == current_user.id).first()
  if not habit:
    raise HTTPException(status_code=404, detail="Habit not found")
  return HabitOut(**{
      "id": str(habit.id),
      "user_id": str(habit.user_id),
      "title": habit.title,
      "frequency": habit.frequency.value,
      "target": habit.target,
      "category": habit.category.value,
      "description": habit.description,
      "created_at": habit.created_at,
  })


@router.put("/{habit_id}", response_model=HabitOut)
def update_habit(habit_id: str, payload: HabitUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  habit = db.query(Habit).filter(Habit.id == UUID(
      habit_id), Habit.user_id == current_user.id).first()
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
  if payload.category is not None:
    try:
      habit.category = Category(payload.category)
    except ValueError:
      raise HTTPException(status_code=422, detail="Invalid category")
  if payload.description is not None:
    habit.description = payload.description
  db.commit()
  db.refresh(habit)
  return HabitOut(**{
      "id": str(habit.id),
      "user_id": str(habit.user_id),
      "title": habit.title,
      "frequency": habit.frequency.value,
      "target": habit.target,
      "category": habit.category.value,
      "description": habit.description,
      "created_at": habit.created_at,
  })


@router.delete("/{habit_id}", status_code=204)
def delete_habit(habit_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  habit = db.query(Habit).filter(Habit.id == UUID(habit_id),
                                 Habit.user_id == current_user.id).first()
  if not habit:
    raise HTTPException(status_code=404, detail="Habit not found")
  db.delete(habit)
  db.commit()
  return None
