"""
Service for creating demo habits for new users
"""

from datetime import datetime
import uuid
from sqlalchemy.orm import Session
from app.models.habit import Habit, Category, Frequency


def setup_initial_habits(user_id: str, db: Session) -> list[Habit]:
  """Create demo habits for a new user"""

  demo_habits_data = [
      {
          "title": "Morning Exercise",
          "description": "Start your day with 30 minutes of physical activity",
          "category": Category.fitness,
          "frequency": Frequency.daily,
          "target": 1
      },
      {
          "title": "Drink Water",
          "description": "Stay hydrated by drinking 8 glasses of water",
          "category": Category.health,
          "frequency": Frequency.daily,
          "target": 8
      },
      {
          "title": "Read Books",
          "description": "Read for at least 20 minutes to expand your knowledge",
          "category": Category.learning,
          "frequency": Frequency.daily,
          "target": 20
      },
      {
          "title": "Meditation",
          "description": "Practice mindfulness and meditation for inner peace",
          "category": Category.mindfulness,
          "frequency": Frequency.daily,
          "target": 10
      },
      {
          "title": "Learn Something New",
          "description": "Spend time learning a new skill or topic",
          "category": Category.learning,
          "frequency": Frequency.weekly,
          "target": 2
      },
      {
          "title": "Cardio Workout",
          "description": "Get your heart pumping with cardio exercises",
          "category": Category.fitness,
          "frequency": Frequency.weekly,
          "target": 3
      },
      {
          "title": "Sleep Early",
          "description": "Go to bed before 11 PM for better rest",
          "category": Category.health,
          "frequency": Frequency.daily,
          "target": 1
      },
      {
          "title": "Practice Gratitude",
          "description": "Write down 3 things you're grateful for each day",
          "category": Category.mindfulness,
          "frequency": Frequency.daily,
          "target": 3
      }
  ]

  created_habits = []

  for habit_data in demo_habits_data:
    habit = Habit(
        user_id=uuid.UUID(user_id),
        title=habit_data["title"],
        description=habit_data["description"],
        category=habit_data["category"],
        frequency=habit_data["frequency"],
        target=habit_data["target"],
        created_at=datetime.now()
    )
    db.add(habit)
    created_habits.append(habit)

  db.commit()
  return created_habits


def has_existing_habits(user_id: str, db: Session) -> bool:
  """Check if user already has habits"""
  return db.query(Habit).filter(Habit.user_id == user_id).count() > 0
