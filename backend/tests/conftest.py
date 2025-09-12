import pytest
import asyncio
from typing import Generator, AsyncGenerator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import create_app
from app.db.base import Base
from app.db.session import get_db
from app.models.user import User
from app.models.habit import Habit, Category, Frequency
from app.models.habit_log import HabitLog
from app.core.security import hash_password


# Test database URL - using in-memory SQLite for fast tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Create test engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def override_get_db():
  """Override the database dependency for testing"""
  db = None
  try:
    db = TestingSessionLocal()
    yield db
  finally:
    if db:
      db.close()


@pytest.fixture(scope="session")
def event_loop():
  """Create an instance of the default event loop for the test session."""
  loop = asyncio.get_event_loop_policy().new_event_loop()
  yield loop
  loop.close()


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
  """Create a fresh database session for each test"""
  # Create tables
  Base.metadata.create_all(bind=engine)

  db = TestingSessionLocal()
  try:
    yield db
  finally:
    db.close()
    # Drop all tables after each test
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
  """Create a test client with database override"""
  app = create_app()
  app.dependency_overrides[get_db] = override_get_db

  # Disable rate limiting for tests
  from app.core.config import settings
  original_rate_limit = settings.rate_limit_enabled
  settings.rate_limit_enabled = False

  # Ensure tables are created
  Base.metadata.create_all(bind=engine)

  with TestClient(app) as test_client:
    yield test_client

  # Restore original rate limiting setting
  settings.rate_limit_enabled = original_rate_limit


@pytest.fixture
def test_user(db_session: Session) -> User:
  """Create a test user"""
  user = User(
      email="test@example.com",
      name="Test User",
      password_hash=hash_password("testpassword123")
  )
  db_session.add(user)
  db_session.commit()
  db_session.refresh(user)
  return user


@pytest.fixture
def test_user_2(db_session: Session) -> User:
  """Create a second test user"""
  user = User(
      email="test2@example.com",
      name="Test User 2",
      password_hash=hash_password("testpassword123")
  )
  db_session.add(user)
  db_session.commit()
  db_session.refresh(user)
  return user


@pytest.fixture
def auth_headers(client: TestClient, test_user: User) -> dict:
  """Get authentication headers for test user"""
  response = client.post("/api/auth/login", json={
      "email": "test@example.com",
      "password": "testpassword123"
  })
  assert response.status_code == 200

  # Extract token from cookie
  cookies = response.cookies
  token = cookies.get("access_token")

  return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def test_habit(db_session: Session, test_user: User) -> Habit:
  """Create a test habit"""
  habit = Habit(
      user_id=test_user.id,
      title="Test Habit",
      description="A test habit",
      category=Category.fitness,
      frequency=Frequency.daily,
      target=1
  )
  db_session.add(habit)
  db_session.commit()
  db_session.refresh(habit)
  return habit


@pytest.fixture
def test_habits(db_session: Session, test_user: User) -> list[Habit]:
  """Create multiple test habits"""
  habits = [
      Habit(
          user_id=test_user.id,
          title="Daily Exercise",
          description="Exercise for 30 minutes",
          category=Category.fitness,
          frequency=Frequency.daily,
          target=1
      ),
      Habit(
          user_id=test_user.id,
          title="Read Books",
          description="Read for 1 hour",
          category=Category.learning,
          frequency=Frequency.daily,
          target=1
      ),
      Habit(
          user_id=test_user.id,
          title="Weekly Review",
          description="Review weekly goals",
          category=Category.productivity,
          frequency=Frequency.weekly,
          target=1
      )
  ]

  for habit in habits:
    db_session.add(habit)
  db_session.commit()

  for habit in habits:
    db_session.refresh(habit)

  return habits


@pytest.fixture
def test_habit_log(db_session: Session, test_user: User, test_habit: Habit) -> HabitLog:
  """Create a test habit log"""
  from datetime import date

  log = HabitLog(
      habit_id=test_habit.id,
      date=date.today(),
      quantity=1
  )
  db_session.add(log)
  db_session.commit()
  db_session.refresh(log)
  return log
