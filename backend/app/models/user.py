import enum
import uuid
from datetime import datetime, timezone, UTC

from sqlalchemy import Boolean, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Provider(str, enum.Enum):
  email = "emil"
  google = "google"
  
  
class User(Base):
  __tablename__ = "users"

  id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  email: Mapped[str] = mapped_column(
      String(255), unique=True, index=True, nullable=False)
  password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
  name: Mapped[str | None] = mapped_column(String(255), nullable=True)
  avatar_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
  google_sub: Mapped[str | None] = mapped_column(String(255), nullable=True)
  provider: Mapped[Provider | None] = mapped_column(Enum(Provider), nullable=True)
  created_at: Mapped[datetime] = mapped_column(
      DateTime(timezone=True), default=lambda: datetime.now(UTC))
  has_password: Mapped[bool | None] = mapped_column(Boolean, default=True, nullable=True)

  habits = relationship("Habit", back_populates="user",
                        cascade="all, delete-orphan")
  badges = relationship("Badge", back_populates="user",
                        cascade="all, delete-orphan")
