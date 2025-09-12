from datetime import datetime, timedelta, timezone, UTC
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
  expire_delta = timedelta(
      minutes=expires_minutes or settings.access_token_expire_minutes)
  to_encode: dict[str, Any] = {"sub": subject,
                               "exp": datetime.now(UTC) + expire_delta}
  if extra:
    to_encode.update(extra)
  # jwt_secret is guaranteed to be non-None due to validation in Settings.__init__
  jwt_secret: str = settings.jwt_secret  # type: ignore
  return jwt.encode(to_encode, jwt_secret, algorithm="HS256")


def decode_token(token: str) -> dict[str, Any]:
  try:
    # jwt_secret is guaranteed to be non-None due to validation in Settings.__init__
    jwt_secret: str = settings.jwt_secret  # type: ignore
    return jwt.decode(token, jwt_secret, algorithms=["HS256"])
  except JWTError as exc:
    raise ValueError("Invalid token") from exc
