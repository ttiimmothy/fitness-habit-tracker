from datetime import datetime, date as dt_date
from typing import Annotated, Optional

from pydantic import BaseModel, Field


UUIDStr = Annotated[str, Field(pattern=r"^[0-9a-fA-F-]{36}$")]

class HabitLogOut(BaseModel):
  id: UUIDStr
  habit_id: UUIDStr
  date: dt_date
  quantity: int
  created_at: datetime


class HabitLogCreate(BaseModel):
  date: Optional[dt_date] | None = None
  quantity: int = 1