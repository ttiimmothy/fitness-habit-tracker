import enum
import uuid
from datetime import datetime, timezone, UTC

from sqlalchemy import String, DateTime, Enum, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Frequency(str, enum.Enum):
  daily = "daily"
  weekly = "weekly"
  monthly = "monthly"


class Category(str, enum.Enum):
  health = "health"
  fitness = "fitness"
  productivity = "productivity"
  learning = "learning"
  mindfulness = "mindfulness"
  social = "social"
  creative = "creative"
  financial = "financial"
  other = "other"


class Habit(Base):
  __tablename__ = "habits"

  id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey(
      "users.id", ondelete="CASCADE"), nullable=False, index=True)
  title: Mapped[str] = mapped_column(String(255), nullable=False)
  frequency: Mapped[Frequency] = mapped_column(Enum(Frequency), nullable=False)
  target: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
  category: Mapped[Category] = mapped_column(
      Enum(Category), nullable=False, default=Category.other)
  description: Mapped[str | None] = mapped_column(String(512), nullable=True)
  created_at: Mapped[datetime] = mapped_column(
      DateTime(timezone=True), default=lambda: datetime.now(UTC))

  user = relationship("User", back_populates="habits")
  logs = relationship("HabitLog", back_populates="habit",
                      cascade="all, delete-orphan")
