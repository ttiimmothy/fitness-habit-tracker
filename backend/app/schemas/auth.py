from typing import Optional

from pydantic import BaseModel, EmailStr

from app.schemas.common import UserOut


class LoginRequest(BaseModel):
  email: EmailStr
  password: str


class TokenResponse(BaseModel):
  # Optional since we now use cookies primarily
  accessToken: Optional[str] = None
  user: UserOut

# BaseModel uses for data validation
class ChangePasswordRequest(BaseModel):
  currentPassword: str
  newPassword: str