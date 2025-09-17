"""Habit completion model for tracking daily completion status."""

import uuid
from datetime import date as dt_date, datetime, timezone, UTC
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

# Forward reference for type hints
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  from app.models.habit import Habit


class HabitCompletion(Base):
  """Model for tracking habit completion status per day."""

  __tablename__ = "habit_completions"

  id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True),
      primary_key=True,
      default=uuid.uuid4
  )
  habit_id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True),
      ForeignKey("habits.id", ondelete="CASCADE"),
      nullable=False
  )
  date: Mapped[dt_date] = mapped_column(Date, nullable=False)
  is_completed: Mapped[bool] = mapped_column(Boolean, nullable=False)
  target_at_time: Mapped[int] = mapped_column(Integer, nullable=False)
  quantity_achieved: Mapped[int] = mapped_column(Integer, nullable=False)
  created_at: Mapped[datetime] = mapped_column(
      DateTime,
      nullable=False,
      default=lambda: datetime.now(UTC)
  )
  updated_at: Mapped[datetime] = mapped_column(
      DateTime,
      nullable=False,
      default=lambda: datetime.now(UTC),
      onupdate=lambda: datetime.now(UTC)
  )

  # Relationships
  habit: Mapped["Habit"] = relationship("Habit", back_populates="completions")

  __table_args__ = (
      UniqueConstraint('habit_id', 'date',
                       name='uq_habit_completions_habit_date'),
  )

  def __repr__(self) -> str:
    return f"<HabitCompletion(habit_id={self.habit_id}, date={self.date}, completed={self.is_completed})>"
