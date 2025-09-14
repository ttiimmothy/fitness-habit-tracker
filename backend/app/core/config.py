from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
  env: str = "dev"
  port: int = 8000
  database_url: str | None = None
  jwt_secret: str | None = None
  access_token_expire_minutes: int = 7 * 24 * 60
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

  @property
  def google_redirect_uri_resolved(self) -> str | None:
    """Get the appropriate Google redirect URI based on environment"""
    if self.google_redirect_uri:
      return self.google_redirect_uri

    # Default redirect URIs based on environment
    if self.env == "dev":
      return "http://localhost:4321/auth/google/callback"
    elif self.env == "prod":
      return "https://yourdomain.com/auth/google/callback"
    else:
      return "http://localhost:4321/auth/google/callback"  # Default to dev

  def get_google_redirect_uri_for_request(self, origin: str | None = None) -> str | None:
    """Get Google redirect URI based on the client request"""
    if self.google_redirect_uri:
      return self.google_redirect_uri

    # Determine environment based on request
    if origin:
      return origin + "/auth/google/callback"

    # Fallback to environment-based logic
    return self.google_redirect_uri_resolved

  model_config = SettingsConfigDict(
    env_file=".env",
    case_sensitive=False
  )


settings = Settings()
