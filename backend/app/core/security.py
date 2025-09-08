from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
  return pwd_context.hash(plain_password)


def verify_password(plain_password: str, password_hash: str) -> bool:
  return pwd_context.verify(plain_password, password_hash)


def create_access_token(subject: str, expires_minutes: Optional[int] = None, extra: dict | None = None) -> str:
  expire_delta = timedelta(minutes=expires_minutes or settings.access_token_expire_minutes)
  to_encode: dict[str, Any] = {"sub": subject, "exp": datetime.now(timezone.utc) + expire_delta}
  if extra:
    to_encode.update(extra)
  return jwt.encode(to_encode, settings.jwt_secret, algorithm="HS256")


def decode_token(token: str) -> dict[str, Any]:
  try:
    return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
  except JWTError as exc:
    raise ValueError("Invalid token") from exc
