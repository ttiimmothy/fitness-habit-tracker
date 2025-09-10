from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
  env: str = "dev"
  port: int = 8000
  database_url: str
  jwt_secret: str
  access_token_expire_minutes: int = 7 * 24 * 60
  client_url: str = "http://localhost:4321"
  redis_url: str = "redis://localhost:6379/0"
  rate_limit_enabled: bool = True

  # oauth stubs
  google_client_id: str | None = None
  google_client_secret: str | None = None
  google_redirect_uri: str | None = None

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    if not self.database_url:
      raise ValueError("DATABASE_URL must be provided")
    if not self.jwt_secret:
      raise ValueError("JWT_SECRET must be provided")

  class Config:
    env_file = ".env"
    case_sensitive = False


settings = Settings()
