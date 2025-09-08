from pydantic_settings import BaseSettings


class Settings(BaseSettings):
  env: str = "dev"
  port: int = 8000
  database_url: str
  jwt_secret: str
  access_token_expire_minutes: int = 60
  client_url: str = "http://localhost:4321"
  redis_url: str = "redis://localhost:6379/0"
  rate_limit_enabled: bool = True

  # oauth stubs
  google_client_id: str | None = None
  google_client_secret: str | None = None
  google_redirect_uri: str | None = None

  class Config:
    env_file = ".env"
    case_sensitive = False


settings = Settings()
