import pytest
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.habit import Habit, Category, Frequency
from app.models.habit_log import HabitLog
from app.core.security import hash_password


class TestUserModel:
  """Test User model"""

  def test_user_creation(self, db_session: Session):
    """Test user creation with all fields"""
    user = User(
        email="test@example.com",
        name="Test User",
        password_hash=hash_password("password123"),
        avatar_url="https://example.com/avatar.jpg"
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.name == "Test User"
    assert user.password_hash is not None
    assert user.avatar_url == "https://example.com/avatar.jpg"
    assert user.created_at is not None

  def test_user_creation_minimal(self, db_session: Session):
    """Test user creation with minimal fields"""
    user = User(
        email="minimal@example.com",
        name="Minimal User",
        password_hash=hash_password("password123")
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.email == "minimal@example.com"
    assert user.name == "Minimal User"
    assert user.avatar_url is None

  def test_user_relationships(self, db_session: Session):
    """Test user relationships with habits and logs"""
    user = User(
        email="reltest@example.com",
        name="Relationship Test",
        password_hash=hash_password("password123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Create habits for the user
    habit1 = Habit(
        user_id=user.id,
        title="Habit 1",
        category=Category.fitness,
        frequency=Frequency.daily,
        target=1
    )
    habit2 = Habit(
        user_id=user.id,
        title="Habit 2",
        category=Category.learning,
        frequency=Frequency.weekly,
        target=2
    )

    db_session.add(habit1)
    db_session.add(habit2)
    db_session.commit()

    # Create logs for the habits
    log1 = HabitLog(
        habit_id=habit1.id,
        date=date.today(),
        quantity=1
    )
    log2 = HabitLog(
        habit_id=habit2.id,
        date=date.today(),
        quantity=2
    )

    db_session.add(log1)
    db_session.add(log2)
    db_session.commit()

    # Test relationships
    assert len(user.habits) == 2

    # Test habit relationships
    assert habit1.user == user
    assert habit2.user == user
    assert len(habit1.logs) == 1
    assert len(habit2.logs) == 1


class TestHabitModel:
  """Test Habit model"""

  def test_habit_creation(self, db_session: Session, test_user: User):
    """Test habit creation with all fields"""
    habit = Habit(
        user_id=test_user.id,
        title="Test Habit",
        description="A test habit description",
        category=Category.fitness,
        frequency=Frequency.daily,
        target=3
    )

    db_session.add(habit)
    db_session.commit()
    db_session.refresh(habit)

    assert habit.id is not None
    assert habit.user_id == test_user.id
    assert habit.title == "Test Habit"
    assert habit.description == "A test habit description"
    assert habit.category == Category.fitness
    assert habit.frequency == Frequency.daily
    assert habit.target == 3
    assert habit.created_at is not None

  def test_habit_creation_minimal(self, db_session: Session, test_user: User):
    """Test habit creation with minimal fields"""
    habit = Habit(
        user_id=test_user.id,
        title="Minimal Habit",
        frequency=Frequency.daily,
        target=1
    )

    db_session.add(habit)
    db_session.commit()
    db_session.refresh(habit)

    assert habit.id is not None
    assert habit.user_id == test_user.id
    assert habit.title == "Minimal Habit"
    assert habit.description is None
    assert habit.category == Category.other  # Default category
    assert habit.frequency == Frequency.daily
    assert habit.target == 1

  def test_habit_categories(self, db_session: Session, test_user: User):
    """Test all habit categories"""
    categories = [
        Category.fitness,
        Category.learning,
        Category.productivity,
        Category.health,
        Category.social,
        Category.other
    ]

    for category in categories:
      habit = Habit(
          user_id=test_user.id,
          title=f"Test {category.value}",
          category=category,
          frequency=Frequency.daily,
          target=1
      )
      db_session.add(habit)

    db_session.commit()

    # Verify all habits were created with correct categories
    habits = db_session.query(Habit).filter(
        Habit.user_id == test_user.id).all()
    assert len(habits) == len(categories)

    for habit in habits:
      assert habit.category in categories

  def test_habit_frequencies(self, db_session: Session, test_user: User):
    """Test all habit frequencies"""
    frequencies = [Frequency.daily, Frequency.weekly, Frequency.monthly]

    for frequency in frequencies:
      habit = Habit(
          user_id=test_user.id,
          title=f"Test {frequency.value}",
          category=Category.other,
          frequency=frequency,
          target=1
      )
      db_session.add(habit)

    db_session.commit()

    # Verify all habits were created with correct frequencies
    habits = db_session.query(Habit).filter(
        Habit.user_id == test_user.id).all()
    assert len(habits) == len(frequencies)

    for habit in habits:
      assert habit.frequency in frequencies

  def test_habit_relationships(self, db_session: Session, test_user: User):
    """Test habit relationships with user and logs"""
    habit = Habit(
        user_id=test_user.id,
        title="Relationship Test",
        category=Category.fitness,
        frequency=Frequency.daily,
        target=1
    )
    db_session.add(habit)
    db_session.commit()
    db_session.refresh(habit)

    # Create logs for the habit
    log1 = HabitLog(
        habit_id=habit.id,
        date=date.today(),
        quantity=1
    )
    log2 = HabitLog(
        habit_id=habit.id,
        date=date.today() - timedelta(days=1),
        quantity=1
    )

    db_session.add(log1)
    db_session.add(log2)
    db_session.commit()

    # Test relationships
    assert habit.user == test_user
    assert len(habit.logs) == 2
    assert log1.habit == habit
    assert log2.habit == habit


class TestHabitLogModel:
  """Test HabitLog model"""

  def test_habit_log_creation(self, db_session: Session, test_user: User, test_habit: Habit):
    """Test habit log creation with all fields"""
    log = HabitLog(
        habit_id=test_habit.id,
        date=date.today(),
        quantity=5
    )

    db_session.add(log)
    db_session.commit()
    db_session.refresh(log)

    assert log.id is not None
    assert log.habit_id == test_habit.id
    assert log.date == date.today()
    assert log.quantity == 5
    assert log.created_at is not None

  def test_habit_log_creation_minimal(self, db_session: Session, test_user: User, test_habit: Habit):
    """Test habit log creation with minimal fields (using defaults)"""
    log = HabitLog(
        habit_id=test_habit.id,
        date=date.today()
    )

    db_session.add(log)
    db_session.commit()
    db_session.refresh(log)

    assert log.id is not None
    assert log.habit_id == test_habit.id
    assert log.date == date.today()
    assert log.quantity == 1  # Default quantity

  def test_habit_log_relationships(self, db_session: Session, test_user: User, test_habit: Habit):
    """Test habit log relationships with habit"""
    log = HabitLog(
        habit_id=test_habit.id,
        date=date.today(),
        quantity=2
    )

    db_session.add(log)
    db_session.commit()
    db_session.refresh(log)

    # Test relationships
    assert log.habit == test_habit
    assert log in test_habit.logs

  def test_habit_log_unique_constraint(self, db_session: Session, test_user: User, test_habit: Habit):
    """Test that habit logs have unique constraint on habit_id and date"""
    # Create first log
    log1 = HabitLog(
        habit_id=test_habit.id,
        date=date.today(),
        quantity=1
    )
    db_session.add(log1)
    db_session.commit()

    # Try to create duplicate log (should fail)
    log2 = HabitLog(
        habit_id=test_habit.id,
        date=date.today(),  # Same date
        quantity=2
    )
    db_session.add(log2)

    with pytest.raises(Exception):  # Should raise integrity error
      db_session.commit()

  def test_habit_log_different_dates(self, db_session: Session, test_user: User, test_habit: Habit):
    """Test that habit logs can exist for different dates"""
    today = date.today()
    yesterday = today - timedelta(days=1)

    log1 = HabitLog(
        habit_id=test_habit.id,
        date=today,
        quantity=1
    )
    log2 = HabitLog(
        habit_id=test_habit.id,
        date=yesterday,
        quantity=2
    )

    db_session.add(log1)
    db_session.add(log2)
    db_session.commit()

    # Both logs should be created successfully
    logs = db_session.query(HabitLog).filter(
        HabitLog.habit_id == test_habit.id
    ).all()

    assert len(logs) == 2
    assert log1 in logs
    assert log2 in logs


class TestModelEnums:
  """Test model enums"""

  def test_category_enum_values(self):
    """Test Category enum values"""
    assert Category.fitness.value == "fitness"
    assert Category.learning.value == "learning"
    assert Category.productivity.value == "productivity"
    assert Category.health.value == "health"
    assert Category.social.value == "social"
    assert Category.other.value == "other"

  def test_frequency_enum_values(self):
    """Test Frequency enum values"""
    assert Frequency.daily.value == "daily"
    assert Frequency.weekly.value == "weekly"
    assert Frequency.monthly.value == "monthly"

  def test_enum_string_conversion(self):
    """Test enum string conversion"""
    assert str(Category.fitness) == "Category.fitness"
    assert str(Frequency.daily) == "Frequency.daily"

  def test_enum_equality(self):
    """Test enum equality"""
    assert Category.fitness == Category.fitness
    assert Category.fitness != Category.learning
    assert Frequency.daily == Frequency.daily
    assert Frequency.daily != Frequency.weekly
