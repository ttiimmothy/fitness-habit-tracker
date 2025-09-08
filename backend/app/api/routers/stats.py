from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.get_current_user import get_current_user
from app.db.session import get_db
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.models.user import User
from app.services.analytics import build_week_overview


router = APIRouter()


@router.get("/overview", response_model=dict)
def overview(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  habit_ids = [h.id for h in db.query(Habit.id).filter(Habit.user_id == current_user.id).all()]
  logs = db.query(HabitLog).filter(HabitLog.habit_id.in_(habit_ids)).all() if habit_ids else []
  return build_week_overview(logs)
