import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.habit_log import HabitLog
from app.models.user import User
from app.models.habit import Habit


class TestLogEndpoints:
  """Test habit logging endpoints"""

  def test_create_log_success(self, client: TestClient, auth_headers: dict, test_habit: Habit):
    """Test successful habit log creation"""
    response = client.post(f"/api/logs/{test_habit.id}/log",
                           json={
                               "quantity": 1
    },
        headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["habit_id"] == str(test_habit.id)
    assert data["quantity"] == 1
    assert data["date"] == date.today().isoformat()
    assert "id" in data
    assert "created_at" in data

  def test_create_log_default_quantity(self, client: TestClient, auth_headers: dict, test_habit: Habit):
    """Test habit log creation with default quantity"""
    response = client.post(f"/api/logs/{test_habit.id}/log",
                           json={},
                           headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 1  # Default quantity

  def test_create_log_multiple_quantity(self, client: TestClient, auth_headers: dict, test_habit: Habit):
    """Test habit log creation with multiple quantity"""
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

    response = client.post(f"/api/logs/{habit_data['id']}/log",
                           json={
                               "quantity": 3
    },
        headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 3

  def test_create_log_exceeds_target(self, client: TestClient, auth_headers: dict, test_habit: Habit):
    """Test habit log creation that exceeds target"""
    response = client.post(f"/api/logs/{test_habit.id}/log",
                           json={
                               "quantity": 5  # Exceeds target of 1
    },
        headers=auth_headers)

    assert response.status_code == 400
    error_data = response.json()
    assert "title" in error_data
    assert "quantity would exceed habit target" in error_data["title"].lower()

  def test_create_log_update_existing(self, client: TestClient, auth_headers: dict, test_habit: Habit):
    """Test creating log when one already exists for today (should update quantity)"""
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

    # Create first log
    response1 = client.post(f"/api/logs/{habit_data['id']}/log",
                            json={
                                "quantity": 1
    },
        headers=auth_headers)
    assert response1.status_code == 200

    # Create second log for same habit and date (should update)
    response2 = client.post(f"/api/logs/{habit_data['id']}/log",
                            json={
                                "quantity": 2
    },
        headers=auth_headers)
    assert response2.status_code == 200

    # Should have updated the existing log, not created a new one
    data = response2.json()
    assert data["quantity"] == 3  # 1 + 2

  def test_create_log_nonexistent_habit(self, client: TestClient, auth_headers: dict):
    """Test log creation for non-existent habit"""
    response = client.post("/api/logs/00000000-0000-0000-0000-000000000000/log",
                           json={
                               "quantity": 1
                           },
                           headers=auth_headers)

    assert response.status_code == 404
    error_data = response.json()
    assert "title" in error_data
    assert "Habit not found" in error_data["title"]

  def test_create_log_wrong_user_habit(self, client: TestClient, test_user_2: User, test_habit: Habit):
    """Test log creation for habit owned by different user"""
    # Login as different user
    login_response = client.post("/api/auth/login", json={
        "email": "test2@example.com",
        "password": "testpassword123"
    })
    assert login_response.status_code == 200

    other_auth_headers = {
        "Authorization": f"Bearer {login_response.cookies.get('access_token')}"}

    response = client.post(f"/api/logs/{test_habit.id}/log",
                           json={
                               "quantity": 1
    },
        headers=other_auth_headers)

    assert response.status_code == 404
    error_data = response.json()
    assert "title" in error_data
    assert "Habit not found" in error_data["title"]

  def test_create_log_unauthenticated(self, client: TestClient, test_habit: Habit):
    """Test log creation without authentication"""
    response = client.post(f"/api/logs/{test_habit.id}/log",
                           json={
                               "quantity": 1
    })

    assert response.status_code == 401

  def test_list_logs_success(self, client: TestClient, auth_headers: dict, test_habit: Habit):
    """Test successful log listing"""
    # Create some logs
    client.post(f"/api/logs/{test_habit.id}/log",
                json={"quantity": 1},
                headers=auth_headers)

    response = client.get(
        f"/api/logs?habit_id={test_habit.id}", headers=auth_headers)

    if response.status_code != 200:
      print(f"Error response: {response.status_code} - {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["habit_id"] == str(test_habit.id)
    assert data[0]["quantity"] == 1

  def test_list_logs_empty(self, client: TestClient, auth_headers: dict, test_habit: Habit):
    """Test log listing with no logs"""
    response = client.get(
        f"/api/logs?habit_id={test_habit.id}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data == []

  def test_list_logs_unauthenticated(self, client: TestClient, test_habit: Habit):
    """Test log listing without authentication"""
    response = client.get(f"/api/logs?habit_id={test_habit.id}")

    assert response.status_code == 401

  def test_today_endpoint_success(self, client: TestClient, auth_headers: dict, test_habits: list[Habit]):
    """Test today endpoint with habits and logs"""
    # Create logs for some habits
    response1 = client.post(f"/api/logs/{test_habits[0].id}/log",
                            json={"quantity": 1},
                            headers=auth_headers)
    assert response1.status_code == 200

    response2 = client.post(f"/api/logs/{test_habits[1].id}/log",
                            json={"quantity": 1},
                            headers=auth_headers)
    assert response2.status_code == 200

    response = client.get("/api/logs/today", headers=auth_headers)

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
    response = client.get("/api/logs/today", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data == []

  def test_today_endpoint_unauthenticated(self, client: TestClient):
    """Test today endpoint without authentication"""
    response = client.get("/api/logs/today")

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
    client.post(f"/api/logs/{habit_data['id']}/log",
                json={"quantity": 1},
                headers=auth_headers)
    client.post(f"/api/logs/{habit_data['id']}/log",
                json={"quantity": 2},
                headers=auth_headers)

    response = client.get("/api/logs/today", headers=auth_headers)

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

  def test_create_log_negative_quantity(self, client: TestClient, auth_headers: dict, test_habit: Habit):
    """Test log creation with negative quantity"""
    response = client.post(f"/api/logs/{test_habit.id}/log",
                           json={
                               "quantity": -1
    },
        headers=auth_headers)

    # API doesn't validate negative quantities, so it should succeed
    assert response.status_code == 200

  def test_create_log_zero_quantity(self, client: TestClient, auth_headers: dict, test_habit: Habit):
    """Test log creation with zero quantity"""
    response = client.post(f"/api/logs/{test_habit.id}/log",
                           json={
                               "quantity": 0
    },
        headers=auth_headers)

    # API doesn't validate zero quantities, so it should succeed
    assert response.status_code == 200

  def test_list_logs_with_date_filter(self, client: TestClient, auth_headers: dict, test_habit: Habit):
    """Test log listing with date filtering"""
    # Create logs for different dates
    today = date.today()
    yesterday = today - timedelta(days=1)

    # Create log for today
    client.post(f"/api/logs/{test_habit.id}/log",
                json={"quantity": 1},
                headers=auth_headers)

    # Manually create log for yesterday (bypassing API validation)
    # Use the test database session from the fixture
    from tests.conftest import TestingSessionLocal
    db = TestingSessionLocal()
    try:
      yesterday_log = HabitLog(
          habit_id=test_habit.id,
          date=yesterday,
          quantity=1
      )
      db.add(yesterday_log)
      db.commit()
    finally:
      db.close()

    # Test listing logs for today
    response = client.get(
        f"/api/logs?habit_id={test_habit.id}&date={today.isoformat()}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["date"] == today.isoformat()

    # Test listing logs for yesterday
    response = client.get(
        f"/api/logs?habit_id={test_habit.id}&date={yesterday.isoformat()}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["date"] == yesterday.isoformat()
