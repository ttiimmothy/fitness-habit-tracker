from collections import defaultdict
from datetime import date, timedelta
from typing import Iterable

from app.models.habit_log import HabitLog


def build_week_overview(logs: Iterable[HabitLog]) -> dict:
  labels = []
  data = []
  today = date.today()
  start = today - timedelta(days=6)
  day_to_count: dict[date, int] = defaultdict(int)
  for l in logs:
    if start <= l.date <= today:
      day_to_count[l.date] += 1
  d = start
  while d <= today:
    labels.append(d.strftime("%a"))
    data.append(day_to_count.get(d, 0))
    d += timedelta(days=1)
  return {"labels": labels, "datasets": [{"label": "Logs", "data": data}]}
