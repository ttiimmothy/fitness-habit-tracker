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
  created_at: datetime


class HabitCreate(BaseModel):
  title: str
  frequency: str
  target: int


class HabitUpdate(BaseModel):
  title: str | None = None
  frequency: str | None = None
  target: int | None = None


class HabitLogOut(BaseModel):
  id: UUIDStr
  habit_id: UUIDStr
  date: date
  created_at: datetime


class HabitLogCreate(BaseModel):
  date: Optional[date] | None = None
