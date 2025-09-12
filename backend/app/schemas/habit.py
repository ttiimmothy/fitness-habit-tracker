from datetime import datetime, date as dt_date
from typing import Annotated, Optional

from pydantic import BaseModel, Field


UUIDStr = Annotated[str, Field(pattern=r"^[0-9a-fA-F-]{36}$")]


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
  target: int = Field(gt=0, description="Target must be positive")
  category: str = "other"
  description: str | None = None


class HabitUpdate(BaseModel):
  title: str | None = None
  frequency: str | None = None
  target: int | None = Field(None, gt=0, description="Target must be positive")
  category: str | None = None
  description: str | None = None