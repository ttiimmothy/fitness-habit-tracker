from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional


class Settings(BaseSettings):
  env: str = "dev"
  port: int = 8000
  database_url: str | None = None
  jwt_secret: str | None = None
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
    # Provide defaults for testing
    if not self.database_url:
      self.database_url = "sqlite:///./test.db"
    if not self.jwt_secret:
      self.jwt_secret = "test-secret-key-for-testing-only"

  model_config = ConfigDict(
      env_file=".env",
      case_sensitive=False
  )


settings = Settings()
