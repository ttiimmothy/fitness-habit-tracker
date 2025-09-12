# ✅ Looks in the same directory as __init__.py
from .user import User        # noqa: F401
# also can
# from app.models.user import User
from .badge import Badge      # noqa: F401
from .habit_log import HabitLog
from .habit import Habit

# from user import User   # ❌ Looks in Python's module search path, not in models/