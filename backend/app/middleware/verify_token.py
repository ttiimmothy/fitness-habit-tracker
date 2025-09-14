from typing import Annotated, Optional
from uuid import UUID

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import get_db
from app.models.user import User


bearer_scheme = HTTPBearer(auto_error=False)


def verify_token(request: Request,db: Annotated[Session, Depends(get_db)], credentials: Annotated[Optional[HTTPAuthorizationCredentials], Depends(bearer_scheme)] = None) -> User:
  token = None

  # Try to get token from cookie first
  token = request.cookies.get("access_token")

  # Fallback to bearer token if no cookie
  if not token and credentials:
    token = credentials.credentials

  if not token:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

  try:
    payload = decode_token(token)
  except ValueError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

  user_id = payload.get("sub")
  if not user_id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

  uid = UUID(user_id)
  user = db.query(User).filter(User.id == uid).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
  return user
