from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from app.api.dependencies.get_current_user import get_current_user
from app.core.security import create_access_token, verify_password, hash_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, ChangePasswordRequest, RegisterRequest
from app.schemas.common import UserOut


router = APIRouter()


@router.post("/login", response_model=dict, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
  user = db.query(User).filter(User.email == payload.email).first()
  if not user or not verify_password(payload.password, user.password_hash):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

  token = create_access_token(str(user.id))

  # Set HTTP-only cookie
  response.set_cookie(
    key="access_token",
    value=token,
    httponly=True,
    secure=True,  # Use HTTPS in production
    samesite="lax",
    max_age=7 * 24 * 60 * 60  # 7 days
  )

  return {
    "user": UserOut(**{
      "id": str(user.id),
      "email": user.email,
      "name": user.name,
      "avatar_url": user.avatar_url,
      "created_at": user.created_at,
    })
  }


@router.get("/me", response_model=dict)
def me(current_user: User = Depends(get_current_user)):
  return {
    "user": UserOut(**{
      "id": str(current_user.id),
      "email": current_user.email,
      "name": current_user.name,
      "avatar_url": current_user.avatar_url,
      "created_at": current_user.created_at,
    })
  }


@router.post("/logout")
def logout(response: Response):
  # Clear the access token cookie
  response.delete_cookie(
    key="access_token",
    httponly=True,
    secure=True,
    samesite="lax"
  )
  return {"message": "Successfully logged out"}


@router.get("/google/login")
def google_login():
  return {"url": "#"}


@router.get("/google/callback")
def google_callback():
  raise HTTPException(status_code=501, detail="Google OAuth not enabled")


@router.post("/change-password")
def change_password(payload: ChangePasswordRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  user = db.query(User).filter(User.id == current_user.id).first()
  
  if not user or not verify_password(payload.currentPassword, user.password_hash):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
  user.password_hash = hash_password(payload.newPassword)
  db.commit()
  return {"message": "password update success"}


@router.post("/register", response_model=dict)
def register(payload: RegisterRequest, response: Response, db: Session = Depends(get_db)):
  user = db.query(User).filter(User.email == payload.email).first()
  
  if user:
    raise HTTPException(status_code=409, detail="This email already register")
  
  new_user = User(name=payload.name, email=payload.email, password_hash=hash_password(payload.password))
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  
  token = create_access_token(str(new_user.id))

  # Set HTTP-only cookie
  response.set_cookie(
    key="access_token",
    value=token,
    httponly=True,
    secure=True,  # Use HTTPS in production
    samesite="lax",
    max_age=7 * 24 * 60 * 60  # 7 days
  )
  
  return {
    "user": UserOut(**{
      "id": str(new_user.id),
      "email": new_user.email,
      "name": new_user.name,
      "avatar_url": new_user.avatar_url,
      "created_at": new_user.created_at,
    })
  }
