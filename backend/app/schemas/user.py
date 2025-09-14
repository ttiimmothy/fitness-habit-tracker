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
  provider: str | None = None
  has_password: bool | None = None