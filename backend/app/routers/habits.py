from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session

from app.middleware.verify_token import verify_token
from app.db.session import get_db
from app.models.habit import Habit, Frequency, Category
from app.models.user import User
from app.schemas.habit import HabitOut, HabitCreate, HabitUpdate
from app.services.completion_service import recalculate_habit_completions, update_habit_completions_for_new_target


router = APIRouter()


@router.get("", response_model=list[HabitOut])
def list_habits(db: Session = Depends(get_db), current_user: User = Depends(verify_token)):
  habits = db.query(Habit).filter(
      Habit.user_id == current_user.id).order_by(Habit.created_at.desc()).all()
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
def create_habit(payload: HabitCreate, db: Session = Depends(get_db), current_user: User = Depends(verify_token)):
  try:
    freq = Frequency(payload.frequency)
  except ValueError:
    raise HTTPException(status_code=422, detail="Invalid frequency")

  try:
    category = Category(payload.category)
  except ValueError:
    raise HTTPException(status_code=422, detail="Invalid category")

  habit = Habit(user_id=current_user.id, title=payload.title, frequency=freq,
                target=payload.target, category=category, description=payload.description)
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
        habit_id: UUID = Path(..., description="Habit ID (UUID)"), db: Session = Depends(get_db), current_user: User = Depends(verify_token)):
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
def update_habit(habit_id: str, payload: HabitUpdate, db: Session = Depends(get_db), current_user: User = Depends(verify_token)):
  habit = db.query(Habit).filter(Habit.id == UUID(
      habit_id), Habit.user_id == current_user.id).first()
  if not habit:
    raise HTTPException(status_code=404, detail="Habit not found")
  # Track if target changed for completion recalculation
  target_changed = False

  if payload.title is not None:
    habit.title = payload.title
  if payload.target is not None:
    if habit.target != payload.target:
      target_changed = True
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

  # Update completions if target changed
  if target_changed:
    try:
      # Use the new function that preserves historical accuracy
      update_habit_completions_for_new_target(db, habit.id, habit.target)
      db.commit()
    except Exception as e:
      # Log error but don't fail the update
      print(
          f"Warning: Failed to update completions for habit {habit.id}: {e}")
      db.rollback()
      db.commit()  # Still save the habit update
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
def delete_habit(habit_id: str, db: Session = Depends(get_db), current_user: User = Depends(verify_token)):
  habit = db.query(Habit).filter(Habit.id == UUID(habit_id),
                                 Habit.user_id == current_user.id).first()
  if not habit:
    raise HTTPException(status_code=404, detail="Habit not found")
  db.delete(habit)
  db.commit()
  return None
