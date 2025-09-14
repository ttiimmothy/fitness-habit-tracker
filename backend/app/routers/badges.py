import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.middleware.get_current_user import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.habit import Habit
from app.models.habit_log import HabitLog
from app.schemas.badge import BadgesResponse, BadgeCategory, Badge as BadgeSchema, BadgeStatus, BadgeCategoryEnum, BadgeProgress
from app.models.badge import Badge, BadgeCategoryEnum as ModelBadgeCategoryEnum
from datetime import datetime, timedelta
from sqlalchemy import func, and_, or_

router = APIRouter()


def get_badge_progress(user_id: uuid.UUID, badge_id: str, db: Session) -> dict | None:
  """Calculate progress for a specific badge"""
  if badge_id == "first_habit":
    habit_count = db.query(Habit).filter(Habit.user_id == user_id).count()
    return {"current": min(habit_count, 1), "target": 1} if habit_count > 0 else None

  elif badge_id == "first_log":
    log_count = db.query(HabitLog).join(
        Habit).filter(Habit.user_id == user_id).count()
    return {"current": min(log_count, 1), "target": 1} if log_count > 0 else None

  elif badge_id == "week_warrior":
    # Check for 7 consecutive days of logging
    today = datetime.now().date()
    consecutive_days = 0
    for i in range(7):
      check_date = today - timedelta(days=i)
      has_log = db.query(HabitLog).join(Habit).filter(
          and_(Habit.user_id == user_id, HabitLog.date == check_date)
      ).first()
      if has_log:
        consecutive_days += 1
      else:
        break
    return {"current": consecutive_days, "target": 7} if consecutive_days > 0 else None

  elif badge_id == "streak_master":
    # Check for 30-day streak
    today = datetime.now().date()
    consecutive_days = 0
    for i in range(30):
      check_date = today - timedelta(days=i)
      has_log = db.query(HabitLog).join(Habit).filter(
          and_(Habit.user_id == user_id, HabitLog.date == check_date)
      ).first()
      if has_log:
        consecutive_days += 1
      else:
        break
    return {"current": consecutive_days, "target": 30} if consecutive_days > 0 else None

  elif badge_id == "workout_warrior":
    # Count workout habit logs (sum of quantities)
    workout_logs = db.query(func.sum(HabitLog.quantity)).join(Habit).filter(
        and_(Habit.user_id == user_id, Habit.category == "fitness")
    ).scalar() or 0
    return {"current": workout_logs, "target": 50} if workout_logs > 0 else None

  elif badge_id == "sharing_champion":
    # This would need to be implemented based on your sharing feature
    return {"current": 0, "target": 10}

  elif badge_id == "perfect_week":
    # Check for 7 consecutive days of completing all habits
    today = datetime.now().date()
    consecutive_days = 0
    for i in range(7):
      check_date = today - timedelta(days=i)
      # Check if all habits were completed on this day
      user_habits = db.query(Habit).filter(Habit.user_id == user_id).all()
      if not user_habits:
        break
      all_completed = True
      for habit in user_habits:
        has_log = db.query(HabitLog).filter(
            and_(HabitLog.habit_id == habit.id, HabitLog.date == check_date)
        ).first()
        if not has_log:
          all_completed = False
          break
      if all_completed:
        consecutive_days += 1
      else:
        break
    return {"current": consecutive_days, "target": 7} if consecutive_days > 0 else None

  elif badge_id == "early_bird":
    # Check for logging before 7 AM
    early_logs = db.query(HabitLog).join(Habit).filter(
        and_(Habit.user_id == user_id, func.extract(
            'hour', HabitLog.created_at) < 7)
    ).count()
    return {"current": min(early_logs, 5), "target": 5} if early_logs > 0 else None

  elif badge_id == "night_owl":
    # Check for logging after 10 PM
    night_logs = db.query(HabitLog).join(Habit).filter(
        and_(Habit.user_id == user_id, func.extract(
            'hour', HabitLog.created_at) >= 22)
    ).count()
    return {"current": min(night_logs, 5), "target": 5} if night_logs > 0 else None

  elif badge_id == "habit_creator":
    # Count total habits created
    habit_count = db.query(Habit).filter(Habit.user_id == user_id).count()
    return {"current": habit_count, "target": 10} if habit_count > 0 else None

  elif badge_id == "cardio_king":
    # Count cardio habit logs
    cardio_logs = db.query(func.sum(HabitLog.quantity)).join(Habit).filter(
        and_(Habit.user_id == user_id, Habit.category == "fitness",
             func.lower(Habit.title).contains("cardio"))
    ).scalar() or 0
    return {"current": cardio_logs, "target": 30} if cardio_logs > 0 else None

  elif badge_id == "flexibility_master":
    # Count flexibility habit logs
    flexibility_logs = db.query(func.sum(HabitLog.quantity)).join(Habit).filter(
        and_(Habit.user_id == user_id,
             or_(func.lower(Habit.title).contains("stretch"),
                 func.lower(Habit.title).contains("yoga"),
                 func.lower(Habit.title).contains("flexibility")))
    ).scalar() or 0
    return {"current": flexibility_logs, "target": 20} if flexibility_logs > 0 else None

  elif badge_id == "meditation_master":
    # Count meditation minutes (assuming quantity represents minutes)
    meditation_minutes = db.query(func.sum(HabitLog.quantity)).join(Habit).filter(
        and_(Habit.user_id == user_id,
             or_(func.lower(Habit.title).contains("meditation"),
                 func.lower(Habit.title).contains("mindfulness")))
    ).scalar() or 0
    return {"current": meditation_minutes, "target": 100} if meditation_minutes > 0 else None

  elif badge_id == "hydration_hero":
    # Check for 14 consecutive days of hydration
    today = datetime.now().date()
    consecutive_days = 0
    for i in range(14):
      check_date = today - timedelta(days=i)
      has_log = db.query(HabitLog).join(Habit).filter(
          and_(Habit.user_id == user_id, HabitLog.date == check_date,
               or_(func.lower(Habit.title).contains("water"),
                   func.lower(Habit.title).contains("hydration")))
      ).first()
      if has_log:
        consecutive_days += 1
      else:
        break
    return {"current": consecutive_days, "target": 14} if consecutive_days > 0 else None

  elif badge_id == "sleep_champion":
    # Check for 21 consecutive days of sleep tracking
    today = datetime.now().date()
    consecutive_days = 0
    for i in range(21):
      check_date = today - timedelta(days=i)
      has_log = db.query(HabitLog).join(Habit).filter(
          and_(Habit.user_id == user_id, HabitLog.date == check_date,
               or_(func.lower(Habit.title).contains("sleep"),
                   func.lower(Habit.title).contains("bedtime")))
      ).first()
      if has_log:
        consecutive_days += 1
      else:
        break
    return {"current": consecutive_days, "target": 21} if consecutive_days > 0 else None

  elif badge_id == "motivator":
    # This would need to be implemented based on your social features
    return {"current": 0, "target": 5}

  elif badge_id == "community_helper":
    # This would need to be implemented based on your social features
    return {"current": 0, "target": 3}

  return None


def get_badge_status(progress: dict | None, badge_id: str) -> BadgeStatus:
  """Determine badge status based on progress"""
  if not progress:
    return BadgeStatus.locked

  if progress["current"] >= progress["target"]:
    return BadgeStatus.earned
  else:
    return BadgeStatus.in_progress


@router.get("/", response_model=BadgesResponse)
def get_badges(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  """Get all badges for the current user with progress and status"""

  # Get all badge templates from database
  badge_templates = db.query(Badge).filter(Badge.user_id.is_(None)).all()

  # Process each badge
  processed_badges = []
  earned_count = 0

  for badge_template in badge_templates:
    progress = get_badge_progress(current_user.id, badge_template.badge_id, db)
    status = get_badge_status(progress, badge_template.badge_id)

    if status == BadgeStatus.earned:
      earned_count += 1

    badge = BadgeSchema(
        id=badge_template.badge_id,
        title=badge_template.title,
        description=badge_template.description,
        category=BadgeCategoryEnum(badge_template.category.value),
        icon_url=badge_template.icon_url,
        emoji=badge_template.emoji,
        status=status,
        progress=BadgeProgress(**progress) if progress else None,
        earned_at=datetime.now() if status == BadgeStatus.earned else None,
        requirements=badge_template.requirements
    )
    processed_badges.append(badge)

  # Group badges by category
  categories = []
  category_data = {
      BadgeCategoryEnum.first_steps: {"name": "First Steps", "emoji": "🌱"},
      BadgeCategoryEnum.consistency: {"name": "Consistency", "emoji": "🔥"},
      BadgeCategoryEnum.special_achievements: {"name": "Special Achievements", "emoji": "⭐"},
      BadgeCategoryEnum.fitness: {"name": "Fitness Focus", "emoji": "💪"},
      BadgeCategoryEnum.wellness: {"name": "Wellness & Mindfulness", "emoji": "🧘"},
      BadgeCategoryEnum.social: {"name": "Social & Community", "emoji": "👥"},
  }

  for category_enum, category_info in category_data.items():
    category_badges = [
        b for b in processed_badges if b.category == category_enum]
    if category_badges:  # Only include categories that have badges
      categories.append(BadgeCategory(
          id=category_enum,
          name=category_info["name"],
          emoji=category_info["emoji"],
          badges=category_badges
      ))

  total_badges = len(processed_badges)
  completion_percentage = int(
      (earned_count / total_badges) * 100) if total_badges > 0 else 0

  return BadgesResponse(
      categories=categories,
      total_badges=total_badges,
      earned_badges=earned_count,
      completion_percentage=completion_percentage
  )
