#!/usr/bin/env python3
"""
Seed script to populate the database with badge definitions.
This script creates all the badge templates that users can earn.
"""

from app.db.session import engine
from app.core.config import settings
from app.db.base import Base
from app.models.badge import Badge, BadgeStatus, BadgeCategoryEnum
from app.db.session import SessionLocal
import sys
import os
from datetime import datetime
from sqlalchemy.orm import Session

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))


# Create all tables
from app.models import user, habit, habit_log, badge  # noqa
Base.metadata.create_all(bind=engine)


def seed_badges():
  """Seed the database with badge definitions"""

  # Define all badges
  badge_definitions = [
      # First Steps
      {
          "badge_id": "first_habit",
          "title": "First Habit",
          "description": "Create your first habit",
          "category": BadgeCategoryEnum.first_steps,
          "icon_url": "https://img.icons8.com/color/48/000000/medal2.png",
          "emoji": "🏆",
          "status": BadgeStatus.locked,
          "requirements": "Create at least 1 habit"
      },
      {
          "badge_id": "first_log",
          "title": "First Log",
          "description": "Log your first habit completion",
          "category": BadgeCategoryEnum.first_steps,
          "icon_url": "https://img.icons8.com/fluency/48/000000/checkmark.png",
          "emoji": "✅",
          "status": BadgeStatus.locked,
          "requirements": "Log at least 1 habit completion"
      },
      {
          "badge_id": "week_warrior",
          "title": "Week Warrior",
          "description": "Complete habits for 7 consecutive days",
          "category": BadgeCategoryEnum.first_steps,
          "icon_url": "https://img.icons8.com/fluency/48/000000/calendar.png",
          "emoji": "📅",
          "status": BadgeStatus.locked,
          "requirements": "Complete habits for 7 consecutive days"
      },

      # Consistency
      {
          "badge_id": "streak_master",
          "title": "Streak Master",
          "description": "Maintain a 30-day streak",
          "category": BadgeCategoryEnum.consistency,
          "icon_url": "https://img.icons8.com/?size=100&id=18515&format=png&color=000000",
          "emoji": "🔥",
          "status": BadgeStatus.locked,
          "requirements": "Maintain a 30-day streak on any habit"
      },
      {
          "badge_id": "monthly_champion",
          "title": "Monthly Champion",
          "description": "Complete all habits for a full month without missing a single day",
          "category": BadgeCategoryEnum.consistency,
          "icon_url": "https://img.icons8.com/fluency/48/000000/trophy.png",
          "emoji": "🏆",
          "status": BadgeStatus.locked,
          "requirements": "Complete all habits for 30 consecutive days"
      },
      {
          "badge_id": "perfect_week",
          "title": "Perfect Week",
          "description": "Complete all habits every day for a week",
          "category": BadgeCategoryEnum.consistency,
          "icon_url": "https://img.icons8.com/fluency/48/000000/star.png",
          "emoji": "⭐",
          "status": BadgeStatus.locked,
          "requirements": "Complete all habits every day for 7 consecutive days"
      },

      # Special Achievements
      {
          "badge_id": "early_bird",
          "title": "Early Bird",
          "description": "Log habits before 7 AM",
          "category": BadgeCategoryEnum.special_achievements,
          "icon_url": "https://img.icons8.com/fluency/48/000000/sun.png",
          "emoji": "🌅",
          "status": BadgeStatus.locked,
          "requirements": "Log habits before 7 AM for 5 days"
      },
      {
          "badge_id": "night_owl",
          "title": "Night Owl",
          "description": "Log habits after 10 PM",
          "category": BadgeCategoryEnum.special_achievements,
          "icon_url": "https://img.icons8.com/fluency/48/000000/moon.png",
          "emoji": "🌙",
          "status": BadgeStatus.locked,
          "requirements": "Log habits after 10 PM for 5 days"
      },
      {
          "badge_id": "habit_creator",
          "title": "Habit Creator",
          "description": "Create 10 different habits",
          "category": BadgeCategoryEnum.special_achievements,
          "icon_url": "https://img.icons8.com/fluency/48/000000/add-property.png",
          "emoji": "📝",
          "status": BadgeStatus.locked,
          "requirements": "Create 10 different habits"
      },

      # Fitness
      {
          "badge_id": "workout_warrior",
          "title": "Workout Warrior",
          "description": "Complete 50 workout sessions",
          "category": BadgeCategoryEnum.fitness,
          "icon_url": "https://img.icons8.com/fluency/48/000000/dumbbell.png",
          "emoji": "💪",
          "status": BadgeStatus.locked,
          "requirements": "Complete 50 workout habit logs"
      },
      {
          "badge_id": "cardio_king",
          "title": "Cardio King",
          "description": "Complete 30 cardio sessions",
          "category": BadgeCategoryEnum.fitness,
          "icon_url": "https://img.icons8.com/fluency/48/000000/running.png",
          "emoji": "🏃",
          "status": BadgeStatus.locked,
          "requirements": "Complete 30 cardio habit logs"
      },
      {
          "badge_id": "flexibility_master",
          "title": "Flexibility Master",
          "description": "Complete 20 stretching sessions",
          "category": BadgeCategoryEnum.fitness,
          "icon_url": "https://img.icons8.com/color/48/000000/yoga.png",
          "emoji": "🧘",
          "status": BadgeStatus.locked,
          "requirements": "Complete 20 stretching habit logs"
      },

      # Wellness
      {
          "badge_id": "meditation_master",
          "title": "Meditation Master",
          "description": "Meditate for 100 total minutes",
          "category": BadgeCategoryEnum.wellness,
          "icon_url": "https://img.icons8.com/?size=100&id=16902&format=png&color=000000",
          "emoji": "🧘",
          "status": BadgeStatus.locked,
          "requirements": "Complete meditation habits totaling 100 minutes"
      },
      {
          "badge_id": "hydration_hero",
          "title": "Hydration Hero",
          "description": "Drink 8 glasses of water for 14 days",
          "category": BadgeCategoryEnum.wellness,
          "icon_url": "https://img.icons8.com/fluency/48/000000/water-bottle.png",
          "emoji": "💧",
          "status": BadgeStatus.locked,
          "requirements": "Complete hydration habits for 14 consecutive days"
      },
      {
          "badge_id": "sleep_champion",
          "title": "Sleep Champion",
          "description": "Get 8+ hours of sleep for 21 days",
          "category": BadgeCategoryEnum.wellness,
          "icon_url": "https://img.icons8.com/fluency/48/000000/sleep.png",
          "emoji": "😴",
          "status": BadgeStatus.locked,
          "requirements": "Complete sleep habits for 21 consecutive days"
      },

      # Social
      {
          "badge_id": "sharing_champion",
          "title": "Sharing Champion",
          "description": "Share your progress 10 times",
          "category": BadgeCategoryEnum.social,
          "icon_url": "https://img.icons8.com/fluency/48/000000/share.png",
          "emoji": "📤",
          "status": BadgeStatus.locked,
          "requirements": "Share progress 10 times"
      },
      {
          "badge_id": "motivator",
          "title": "Motivator",
          "description": "Encourage 5 other users",
          "category": BadgeCategoryEnum.social,
          "icon_url": "https://img.icons8.com/ios-filled/50/000000/conference-call.png",
          "emoji": "👥",
          "status": BadgeStatus.locked,
          "requirements": "Encourage 5 other users"
      },
      {
          "badge_id": "community_helper",
          "title": "Community Helper",
          "description": "Help 3 users with their habits by providing encouragement and support",
          "category": BadgeCategoryEnum.social,
          "icon_url": "https://img.icons8.com/fluency/48/000000/help.png",
          "emoji": "🤝",
          "status": BadgeStatus.locked,
          "requirements": "Help 3 users with their habits"
      }
  ]

  db = SessionLocal()
  try:
    # Clear existing badges (optional - remove if you want to keep existing data)
    db.query(Badge).delete()
    db.commit()

    # Insert badge definitions
    for badge_data in badge_definitions:
      badge = Badge(
          badge_id=badge_data["badge_id"],
          title=badge_data["title"],
          description=badge_data["description"],
          category=badge_data["category"],
          icon_url=badge_data["icon_url"],
          emoji=badge_data["emoji"],
          status=badge_data["status"],
          requirements=badge_data["requirements"],
          created_at=datetime.now()
      )
      db.add(badge)

    db.commit()
    print(f"✅ Successfully seeded {len(badge_definitions)} badges!")

    # Print summary by category
    categories = {}
    for badge_data in badge_definitions:
      category = badge_data["category"].value
      if category not in categories:
        categories[category] = 0
      categories[category] += 1

    print("\n📊 Badge Summary by Category:")
    for category, count in categories.items():
      print(f"  {category}: {count} badges")

  except Exception as e:
    print(f"❌ Error seeding badges: {e}")
    db.rollback()
  finally:
    db.close()


if __name__ == "__main__":
  seed_badges()
