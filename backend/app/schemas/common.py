from datetime import datetime, date
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
  date: date
  created_at: datetime


class HabitLogCreate(BaseModel):
  date: Optional[datetime] | None = None


class DailyLogCount(BaseModel):
  date: date
  count: int


class HabitStats(BaseModel):
  habit_id: UUIDStr
  total_logs: int
  current_streak: int
  longest_streak: int
  completion_rate: float  # percentage
  last_log_date: date | None = None


class HabitDailyProgress(BaseModel):
  date: date
  completed: bool
  target: int
  actual: int
