import uuid
from datetime import date as dt_date, datetime, timezone, UTC

from sqlalchemy import Date, DateTime, ForeignKey, UniqueConstraint, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class HabitLog(Base):
  __tablename__ = "habit_logs"
  __table_args__ = (
      UniqueConstraint("habit_id", "date", name="uq_habit_date"),
  )

  id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  habit_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey(
      "habits.id", ondelete="CASCADE"), nullable=False, index=True)
  date: Mapped[dt_date] = mapped_column(Date, nullable=False)
  quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
  created_at: Mapped[datetime] = mapped_column(
      DateTime(timezone=True), default=lambda: datetime.now(UTC))

  habit = relationship("Habit", back_populates="logs")
