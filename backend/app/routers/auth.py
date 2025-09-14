import requests

from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from fastapi_limiter.depends import RateLimiter
from app.core.config import settings
from sqlalchemy.orm import Session

from app.api.middleware.get_current_user import get_current_user
from app.core.security import create_access_token, verify_password, hash_password
from app.db.session import get_db
from app.lib.get_or_create_user import get_or_create_user
from app.models.user import Provider, User
from app.schemas.auth import GoogleLoginRequest, LoginRequest, ChangePasswordRequest, RegisterRequest, SetupPasswordPayload, UploadProfileRequest
from app.schemas.user import UserOut
from app.services.setup_initial_habits import setup_initial_habits, has_existing_habits
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

router = APIRouter()


@router.post("/login", response_model=dict)
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

    # samesite="lax"
    samesite="none",
    max_age=settings.access_token_expire_minutes * 60  # Same as JWT token expiration
  )

  return {
    "user": UserOut(**{
      "id": str(user.id),
      "email": user.email,
      "name": user.name,
      "avatar_url": user.avatar_url,
      "created_at": user.created_at,

      "provider": user.provider,
      "has_password": user.has_password
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

      "provider": current_user.provider,
      "has_password": current_user.has_password
    })
  }


@router.post("/logout")
def logout(response: Response):
  # Clear the access token cookie
  response.delete_cookie(
    key="access_token",
    httponly=True,
    secure=True,
    # samesite="lax"
    samesite="none"
  )
  return {"message": "Successfully logged out"}


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

  new_user = User(name=payload.name, email=payload.email, password_hash=hash_password(payload.password), provider=Provider.email)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)

  # Create demo habits for new user
  setup_initial_habits(str(new_user.id), db)

  token = create_access_token(str(new_user.id))

  # Set HTTP-only cookie
  response.set_cookie(
      key="access_token",
      value=token,
      httponly=True,
      secure=True,  # Use HTTPS in production
      samesite="none",
      max_age=settings.access_token_expire_minutes * 60
  )

  return {
    "user": UserOut(**{
      "id": str(new_user.id),
      "email": new_user.email,
      "name": new_user.name,
      "avatar_url": new_user.avatar_url,
      "created_at": new_user.created_at,
      "provider": new_user.provider,
      "has_password": new_user.has_password
    })
  }


@router.put("/update-profile")
def update_profile(payload: UploadProfileRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  user = db.query(User).filter(User.id == current_user.id).first()

  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No this user")

  user.name = payload.name
  db.commit()
  db.refresh(user)
  return {"name": user.name}


@router.post("/google", response_model=dict)
def google_auth(payload: GoogleLoginRequest, request: Request, response: Response, db: Session = Depends(get_db)):
  try:
    # Check required environment variables
    # client_id = settings.google_client_id
    # client_secret = settings.google_client_secret

    # Get redirect URI based on request
    # host = request.headers.get("host")
    origin = request.headers.get("origin")
    redirect_uri = settings.get_google_redirect_uri_for_request(origin=origin)
    # print(
    #     f"Env vars - client_id: {bool(client_id)}, client_secret: {bool(client_secret)}, redirect_uri: {bool(redirect_uri)}")

    # Exchange authorization code for tokens
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
      "client_id": settings.google_client_id,
      "client_secret": settings.google_client_secret,
      "code": payload.code,
      "grant_type": "authorization_code",
      "redirect_uri": redirect_uri
    }

    token_response = requests.post(token_url, data=token_data)
    token_response.raise_for_status()
    tokens = token_response.json()

    # Verify the ID token
    idinfo = id_token.verify_oauth2_token(
      tokens["id_token"],
      google_requests.Request(),
      settings.google_client_id
    )

    # Extract user information
    user_id = idinfo["sub"]
    user_name = idinfo["name"]
    user_email = idinfo["email"]
    user_picture = idinfo["picture"]

    user = get_or_create_user(db, user_id, user_name, user_email, user_picture)

    # Create demo habits for new Google users (check if they have existing habits)
    if not has_existing_habits(str(user.id), db):
      setup_initial_habits(str(user.id), db)

    token = create_access_token(str(user.id))

    response.set_cookie(
      key="access_token",
      value=token,
      httponly=True,
      secure=True,  # Use HTTPS in production
      samesite="none",
      max_age=settings.access_token_expire_minutes * 60
    )

    return {
      "user": UserOut(**{
        "id": str(user.id),
        "email": user.email,
        "name": user.name,
        "avatar_url": user.avatar_url,
        "created_at": user.created_at,
        "provider": user.provider,
        "has_password": user.has_password
      })
    }

  except requests.exceptions.RequestException as e:
    raise HTTPException(status_code=400, detail=f"Google OAuth request failed: {str(e)}")
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")


@router.post("/setup-password")
def setup_password(payload: SetupPasswordPayload, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  user = db.query(User).filter(User.id == current_user.id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Can't find this user")
  user.password_hash = hash_password(payload.password)
  user.has_password = True
  db.commit()
  db.refresh(user)
  return {"message": "password setup success"}
