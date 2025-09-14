import uuid
from datetime import datetime, timezone, UTC
from enum import Enum

from sqlalchemy import String, DateTime, ForeignKey, Enum as SQLEnum, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


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


class Badge(Base):
  __tablename__ = "badges"

  id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey(
      "users.id", ondelete="CASCADE"), nullable=True, index=True)
  badge_id: Mapped[str] = mapped_column(
      String(64), nullable=False)  # e.g., "first_habit"
  title: Mapped[str] = mapped_column(String(255), nullable=False)
  description: Mapped[str] = mapped_column(Text, nullable=False)
  category: Mapped[BadgeCategoryEnum] = mapped_column(
      SQLEnum(BadgeCategoryEnum), nullable=False)
  icon_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
  emoji: Mapped[str | None] = mapped_column(String(10), nullable=True)
  status: Mapped[BadgeStatus] = mapped_column(
      SQLEnum(BadgeStatus), nullable=False, default=BadgeStatus.locked)
  progress_current: Mapped[int | None] = mapped_column(Integer, nullable=True)
  progress_target: Mapped[int | None] = mapped_column(Integer, nullable=True)
  earned_at: Mapped[datetime | None] = mapped_column(
      DateTime(timezone=True), nullable=True)
  requirements: Mapped[str | None] = mapped_column(Text, nullable=True)
  created_at: Mapped[datetime] = mapped_column(
      DateTime(timezone=True), default=lambda: datetime.now(UTC))

  user = relationship("User", back_populates="badges")
