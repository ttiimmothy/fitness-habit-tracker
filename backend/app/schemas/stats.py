from datetime import datetime, date as dt_date
from typing import Annotated, Optional

from pydantic import BaseModel, Field


UUIDStr = Annotated[str, Field(pattern=r"^[0-9a-fA-F-]{36}$")]


class DailyLogCount(BaseModel):
  date: dt_date
  count: int
  

class HabitStats(BaseModel):
  habit_id: UUIDStr
  current_streak: int
  longest_streak: int
  completion_rate: float


class HabitDailyProgress(BaseModel):
  date: dt_date
  completed: bool
  target: int
  actual: int


class TodayHabitLog(BaseModel):
  habit_id: UUIDStr
  title: str
  category: str
  frequency: str
  target: int
  logged_today: bool
  current_progress: int  # How many times logged today
  log_id: UUIDStr | None = None
  log_created_at: datetime | None = None