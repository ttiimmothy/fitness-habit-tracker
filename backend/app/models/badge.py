import uuid
from datetime import datetime, timezone, UTC

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Badge(Base):
  __tablename__ = "badges"

  id: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey(
      "users.id", ondelete="CASCADE"), nullable=False, index=True)
  code: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
  achieved_at: Mapped[datetime] = mapped_column(
      DateTime(timezone=True), default=lambda: datetime.now(UTC))

  user = relationship("User", back_populates="badges")
