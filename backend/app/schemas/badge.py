from datetime import datetime
from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field


class BadgeStatus(str, Enum):
  earned = "earned"
  in_progress = "in_progress"
  locked = "locked"


class BadgeCategoryEnum(str, Enum):
  first_steps = "first_steps"
  consistency = "consistency"
  special_achievements = "special_achievements"
  wellness = "wellness"
  fitness = "fitness"
  social = "social"


class BadgeProgress(BaseModel):
  current: int
  target: int


class Badge(BaseModel):
  id: str
  title: str
  description: str
  category: BadgeCategoryEnum
  icon_url: Optional[str] = None
  emoji: Optional[str] = None
  status: BadgeStatus
  progress: Optional[BadgeProgress] = None
  earned_at: Optional[datetime] = None
  requirements: Optional[str] = None


class BadgeCategory(BaseModel):
  id: BadgeCategoryEnum
  name: str
  emoji: str
  badges: list[Badge]


class BadgesResponse(BaseModel):
  categories: list[BadgeCategory]
  total_badges: int
  earned_badges: int
  completion_percentage: int
