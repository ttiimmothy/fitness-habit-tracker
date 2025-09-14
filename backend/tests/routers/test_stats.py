import pytest
import uuid
from datetime import date, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.habit_log import HabitLog
from app.models.habit import Habit
from app.models.user import User


class TestStatsEndpoints:
  """Test statistics endpoints"""

  # def test_daily_counts_success(self, client: TestClient, auth_headers: dict, test_habits: list[Habit]):
  #   """Test daily counts endpoint with logs"""
  #   # Create logs for different habits
  #   client.post(f"/api/logs/habits/{test_habits[0].id}/log",
  #               json={"quantity": 1},
  #               headers=auth_headers)
  #   client.post(f"/api/logs/habits/{test_habits[1].id}/log",
  #               json={"quantity": 1},
  #               headers=auth_headers)

  #   response = client.get("/api/stats/daily-counts", headers=auth_headers)

  #   assert response.status_code == 200
  #   data = response.json()
  #   assert len(data) == 30  # Default 30 days

  #   # Find today's entry
  #   today_entry = next(
  #       (entry for entry in data if entry["date"] == date.today().isoformat()), None)
  #   assert today_entry is not None
  #   assert today_entry["count"] == 2  # 2 habits logged today

  # def test_daily_counts_empty(self, client: TestClient, auth_headers: dict):
  #   """Test daily counts endpoint with no logs"""
  #   response = client.get("/api/stats/daily-counts", headers=auth_headers)

  #   assert response.status_code == 200
  #   data = response.json()
  #   assert len(data) == 30  # Default 30 days, all with count 0
  #   assert all(entry["count"] == 0 for entry in data)

  # def test_daily_counts_unauthenticated(self, client: TestClient):
  #   """Test daily counts endpoint without authentication"""
  #   response = client.get("/api/stats/daily-counts")

  #   assert response.status_code == 401

  # def test_daily_counts_multiple_days(self, client: TestClient, auth_headers: dict, test_habits: list[Habit], db_session: Session):
  #   """Test daily counts across multiple days"""
  #   # Create logs for different days
  #   today = date.today()
  #   yesterday = today - timedelta(days=1)

  #   # Today's logs
  #   client.post(f"/api/logs/habits/{test_habits[0].id}/log",
  #               json={"quantity": 1},
  #               headers=auth_headers)

  #   # Yesterday's logs (manually created)
  #   for habit in test_habits[:2]:
  #     log = HabitLog(
  #         habit_id=habit.id,
  #         date=yesterday,
  #         quantity=1
  #     )
  #     db_session.add(log)
  #   db_session.commit()

  #   response = client.get("/api/stats/daily-counts", headers=auth_headers)

  #   assert response.status_code == 200
  #   data = response.json()
  #   assert len(data) == 30  # Default 30 days

  #   # Check today's count
  #   today_data = next(
  #       item for item in data if item["date"] == today.isoformat())
  #   assert today_data["count"] == 1

  #   # Check yesterday's count
  #   yesterday_data = next(
  #       item for item in data if item["date"] == yesterday.isoformat())
  #   assert yesterday_data["count"] == 2

  def test_habit_streak_stats_success(self, client: TestClient, auth_headers: dict, test_habit: Habit, db_session: Session):
    """Test habit streak statistics"""
    # Create logs for consecutive days
    today = date.today()
    for i in range(5):
      log_date = today - timedelta(days=i)
      log = HabitLog(
          habit_id=test_habit.id,
          date=log_date,
          quantity=1
      )
      db_session.add(log)
    db_session.commit()

    response = client.get(
        f"/api/stats/{test_habit.id}/stats/streak", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["habit_id"] == str(test_habit.id)
    assert data["current_streak"] == 5
    assert data["longest_streak"] == 5

  def test_habit_streak_stats_broken_streak(self, client: TestClient, auth_headers: dict, test_habit: Habit, db_session: Session):
    """Test habit streak with broken streak"""
    # Create logs with a gap
    today = date.today()
    dates = [today, today - timedelta(days=1), today -
             timedelta(days=3), today - timedelta(days=4)]

    for log_date in dates:
      log = HabitLog(
          habit_id=test_habit.id,
          date=log_date,
          quantity=1
      )
      db_session.add(log)
    db_session.commit()

    response = client.get(
        f"/api/stats/{test_habit.id}/stats/streak", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["current_streak"] == 2  # Only last 2 days
    assert data["longest_streak"] == 2  # Longest consecutive is 2

  def test_habit_streak_stats_insufficient_quantity(self, client: TestClient, auth_headers: dict, test_habit: Habit, db_session: Session):
    """Test habit streak with insufficient quantity (less than target)"""
    # Create logs with quantity less than target
    today = date.today()
    for i in range(3):
      log_date = today - timedelta(days=i)
      log = HabitLog(
          habit_id=test_habit.id,
          date=log_date,
          quantity=0  # Less than target of 1
      )
      db_session.add(log)
    db_session.commit()

    response = client.get(
        f"/api/stats/{test_habit.id}/stats/streak", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["current_streak"] == 0  # No valid streaks
    assert data["longest_streak"] == 0

  def test_habit_streak_stats_nonexistent_habit(self, client: TestClient, auth_headers: dict):
    """Test streak stats for non-existent habit"""
    fake_uuid = str(uuid.uuid4())
    response = client.get(
        f"/api/stats/{fake_uuid}/stats/streak", headers=auth_headers)

    assert response.status_code == 404
    error_data = response.json()
    assert "Habit not found" in error_data["title"]

  def test_habit_streak_stats_wrong_user(self, client: TestClient, test_user_2: User, test_habit: Habit):
    """Test streak stats for habit owned by different user"""
    # Login as different user
    login_response = client.post("/api/auth/login", json={
        "email": "test2@example.com",
        "password": "testpassword123"
    })
    assert login_response.status_code == 200

    other_auth_headers = {
        "Authorization": f"Bearer {login_response.cookies.get('access_token')}"}

    response = client.get(
        f"/api/stats/{test_habit.id}/stats/streak", headers=other_auth_headers)

    assert response.status_code == 404
    error_data = response.json()
    assert "Habit not found" in error_data["title"]

  def test_habit_daily_progress_success(self, client: TestClient, auth_headers: dict, test_habit: Habit, db_session: Session):
    """Test habit daily progress endpoint"""
    # Create logs for different days
    today = date.today()
    for i in range(7):
      log_date = today - timedelta(days=i)
      log = HabitLog(
          habit_id=test_habit.id,
          date=log_date,
          quantity=1 if i % 2 == 0 else 0  # Every other day
      )
      db_session.add(log)
    db_session.commit()

    response = client.get(
        f"/api/stats/{test_habit.id}/daily-progress?days=7", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 7

    # Check that we have data for each day
    dates = [item["date"] for item in data]
    for i in range(7):
      expected_date = (today - timedelta(days=i)).isoformat()
      assert expected_date in dates

  def test_habit_daily_progress_default_days(self, client: TestClient, auth_headers: dict, test_habit: Habit):
    """Test habit daily progress with default days parameter"""
    response = client.get(
        f"/api/stats/{test_habit.id}/daily-progress", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 7  # Default 7 days

  def test_habit_daily_progress_custom_days(self, client: TestClient, auth_headers: dict, test_habit: Habit):
    """Test habit daily progress with custom days parameter"""
    response = client.get(
        f"/api/stats/{test_habit.id}/daily-progress?days=14", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 14

  def test_habit_daily_progress_with_quantities(self, client: TestClient, auth_headers: dict, test_habit: Habit, db_session: Session):
    """Test habit daily progress shows correct quantities"""
    # Create logs with different quantities
    today = date.today()
    # Day 1: quantity 2
    log1 = HabitLog(
        habit_id=test_habit.id,
        date=today,
        quantity=2
    )
    db_session.add(log1)

    # Day 2: quantity 1
    log2 = HabitLog(
        habit_id=test_habit.id,
        date=today - timedelta(days=1),
        quantity=1
    )
    db_session.add(log2)

    db_session.commit()

    response = client.get(
        f"/api/stats/{test_habit.id}/daily-progress?days=2", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    # Check today's data
    today_data = next(
        item for item in data if item["date"] == today.isoformat())
    assert today_data["completed"] is True
    assert today_data["target"] == 1
    assert today_data["actual"] == 2

    # Check yesterday's data
    yesterday_data = next(item for item in data if item["date"] == (
        today - timedelta(days=1)).isoformat())
    assert yesterday_data["completed"] is True
    assert yesterday_data["target"] == 1
    assert yesterday_data["actual"] == 1

  def test_habit_daily_progress_nonexistent_habit(self, client: TestClient, auth_headers: dict):
    """Test daily progress for non-existent habit"""
    fake_uuid = str(uuid.uuid4())
    response = client.get(
        f"/api/stats/{fake_uuid}/daily-progress", headers=auth_headers)

    assert response.status_code == 404
    error_data = response.json()
    assert "Habit not found" in error_data["title"]

  def test_habit_daily_progress_wrong_user(self, client: TestClient, test_user_2: User, test_habit: Habit):
    """Test daily progress for habit owned by different user"""
    # Login as different user
    login_response = client.post("/api/auth/login", json={
        "email": "test2@example.com",
        "password": "testpassword123"
    })
    assert login_response.status_code == 200

    other_auth_headers = {
        "Authorization": f"Bearer {login_response.cookies.get('access_token')}"}

    response = client.get(
        f"/api/stats/{test_habit.id}/daily-progress", headers=other_auth_headers)

    assert response.status_code == 404
    error_data = response.json()
    assert "Habit not found" in error_data["title"]

  def test_habit_daily_progress_invalid_days(self, client: TestClient, auth_headers: dict, test_habit: Habit):
    """Test daily progress with invalid days parameter"""
    response = client.get(
        f"/api/stats/{test_habit.id}/daily-progress?days=0", headers=auth_headers)

    assert response.status_code == 422  # Validation error

  def test_habit_daily_progress_negative_days(self, client: TestClient, auth_headers: dict, test_habit: Habit):
    """Test daily progress with negative days parameter"""
    response = client.get(
        f"/api/stats/{test_habit.id}/daily-progress?days=-1", headers=auth_headers)

    assert response.status_code == 422  # Validation error

  def test_habit_daily_progress_large_days(self, client: TestClient, auth_headers: dict, test_habit: Habit):
    """Test daily progress with very large days parameter"""
    response = client.get(
        f"/api/stats/{test_habit.id}/daily-progress?days=1000", headers=auth_headers)

    assert response.status_code == 422  # Validation error for too large days

  def test_today_endpoint_success(self, client: TestClient, auth_headers: dict, test_habits: list[Habit]):
    """Test today endpoint with habits and logs"""
    # Create logs for some habits
    response1 = client.post(f"/api/logs/habits/{test_habits[0].id}/log",
                            json={"quantity": 1},
                            headers=auth_headers)
    assert response1.status_code == 200

    response2 = client.post(f"/api/logs/habits/{test_habits[1].id}/log",
                            json={"quantity": 1},
                            headers=auth_headers)
    assert response2.status_code == 200

    response = client.get("/api/stats/logs/today", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3  # All 3 test habits

    # Check that habits are included
    habit_ids = [habit["habit_id"] for habit in data]
    assert str(test_habits[0].id) in habit_ids
    assert str(test_habits[1].id) in habit_ids
    assert str(test_habits[2].id) in habit_ids

    # Check logged habits have correct data
    logged_habits = [h for h in data if h["logged_today"]]
    assert len(logged_habits) == 2

    for habit in logged_habits:
      assert habit["current_progress"] > 0
      assert habit["log_id"] is not None
      assert habit["log_created_at"] is not None

    # Check unlogged habits
    unlogged_habits = [h for h in data if not h["logged_today"]]
    assert len(unlogged_habits) == 1
    assert unlogged_habits[0]["current_progress"] == 0
    assert unlogged_habits[0]["log_id"] is None
    assert unlogged_habits[0]["log_created_at"] is None

  def test_today_endpoint_empty_habits(self, client: TestClient, auth_headers: dict):
    """Test today endpoint with no habits"""
    response = client.get("/api/stats/logs/today", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data == []

  def test_today_endpoint_unauthenticated(self, client: TestClient):
    """Test today endpoint without authentication"""
    response = client.get("/api/stats/logs/today")

    assert response.status_code == 401

  def test_today_endpoint_multiple_logs_same_habit(self, client: TestClient, auth_headers: dict, test_habit: Habit):
    """Test today endpoint with multiple logs for same habit (should sum quantities)"""
    # First create a habit with higher target for this test
    habit_response = client.post("/api/habits",
                                 json={
                                     "title": "High Target Habit",
                                     "description": "A habit with high target",
                                     "category": "fitness",
                                     "frequency": "daily",
                                     "target": 5
                                 },
                                 headers=auth_headers)
    assert habit_response.status_code == 201
    habit_data = habit_response.json()

    # Create multiple logs for same habit
    client.post(f"/api/logs/habits/{habit_data['id']}/log",
                json={"quantity": 1},
                headers=auth_headers)
    client.post(f"/api/logs/habits/{habit_data['id']}/log",
                json={"quantity": 2},
                headers=auth_headers)

    response = client.get("/api/stats/logs/today", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()

    # Find the habit we created (should have current_progress of 3)
    habit_data = None
    for habit in data:
      if habit["current_progress"] == 3:
        habit_data = habit
        break

    assert habit_data is not None, "Could not find habit with current_progress of 3"
    assert habit_data["logged_today"] is True
    assert habit_data["current_progress"] == 3  # 1 + 2
    assert habit_data["log_id"] is not None

  def test_overview_calendar_endpoint_success(self, client: TestClient, auth_headers: dict, test_habits: list[Habit]):
    """Test overview calendar endpoint with habits and logs"""
    # Create logs for different habits (both on same date)
    client.post(f"/api/logs/habits/{test_habits[0].id}/log",
                json={"quantity": 1},
                headers=auth_headers)
    client.post(f"/api/logs/habits/{test_habits[1].id}/log",
                json={"quantity": 1},
                headers=auth_headers)

    response = client.get("/api/stats/overview/calendar", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()

    # Check response structure - now it's a list of DayLogs directly
    assert isinstance(data, list)
    assert len(data) >= 1

    # Check first day entry structure
    if data:
      first_day = data[0]
      assert "date" in first_day
      assert "habits" in first_day
      assert "totalLogs" in first_day
      assert isinstance(first_day["habits"], list)
      assert first_day["totalLogs"] >= 2  # Should have both habits for today

      # Check habit entry structure
      if first_day["habits"]:
        first_habit = first_day["habits"][0]
        assert "habit_id" in first_habit
        assert "habit_title" in first_habit
        assert "quantity" in first_habit
        assert "target" in first_habit
        assert "logged_at" in first_habit

  def test_overview_calendar_endpoint_empty(self, client: TestClient, auth_headers: dict):
    """Test overview calendar endpoint with no habits"""
    response = client.get("/api/stats/overview/calendar", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()

    assert data == []

  def test_overview_calendar_endpoint_unauthenticated(self, client: TestClient):
    """Test overview calendar endpoint without authentication"""
    response = client.get("/api/stats/overview/calendar")

    assert response.status_code == 401
