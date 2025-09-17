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
  # Target that was in effect during this period
  effective_target: int | None = None


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


class HabitLogEntry(BaseModel):
  habit_id: UUIDStr
  habit_title: str
  quantity: int
  target: int
  logged_at: datetime


class DayLogs(BaseModel):
  date: dt_date
  habits: list[HabitLogEntry]
  totalLogs: int


class OverviewResponse(BaseModel):
  logs: list[DayLogs]
  total_days: int
  total_logs: int
