from datetime import datetime, date as dt_date
from typing import Annotated, Optional

from pydantic import BaseModel, Field


UUIDStr = Annotated[str, Field(pattern=r"^[0-9a-fA-F-]{36}$")]


class UserOut(BaseModel):
  id: UUIDStr
  email: str
  name: str | None = None
  avatar_url: str | None = None
  created_at: datetime


class HabitOut(BaseModel):
  id: UUIDStr
  user_id: UUIDStr
  title: str
  frequency: str
  target: int
  category: str
  description: str | None
  created_at: datetime


class HabitCreate(BaseModel):
  title: str
  frequency: str
  target: int
  category: str = "other"
  description: str | None


class HabitUpdate(BaseModel):
  title: str | None = None
  frequency: str | None = None
  target: int | None = None
  category: str | None = None
  description: str | None = None


class HabitLogOut(BaseModel):
  id: UUIDStr
  habit_id: UUIDStr
  date: dt_date
  quantity: int
  created_at: datetime


class HabitLogCreate(BaseModel):
  date: Optional[dt_date] | None = None
  quantity: int = 1


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
