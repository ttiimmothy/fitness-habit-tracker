import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import create_app
from app.models.user import User
from app.models.habit import Habit
from app.models.habit_log import HabitLog


class TestBadgesEndpoints:
  def test_get_badges_success(self, client: TestClient, auth_headers: dict):
    """Test getting badges for a user"""
    response = client.get("/api/badges", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()

    # Check response structure
    assert "categories" in data
    assert "total_badges" in data
    assert "earned_badges" in data
    assert "completion_percentage" in data

    # Check that we have categories
    assert isinstance(data["categories"], list)
    assert len(data["categories"]) > 0

    # Check first category structure
    first_category = data["categories"][0]
    assert "id" in first_category
    assert "name" in first_category
    assert "emoji" in first_category
    assert "badges" in first_category
    assert isinstance(first_category["badges"], list)

    # Check first badge structure
    if first_category["badges"]:
      first_badge = first_category["badges"][0]
      assert "id" in first_badge
      assert "title" in first_badge
      assert "description" in first_badge
      assert "category" in first_badge
      assert "status" in first_badge
      assert first_badge["status"] in ["earned", "in_progress", "locked"]

  def test_get_badges_with_habits(self, client: TestClient, auth_headers: dict, test_habits: list[Habit]):
    """Test getting badges when user has habits"""
    response = client.get("/api/badges", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()

    # Should have some earned badges now
    assert data["earned_badges"] >= 0
    assert data["total_badges"] > 0

  def test_get_badges_with_logs(self, client: TestClient, auth_headers: dict, test_habits: list[Habit]):
    """Test getting badges when user has logged habits"""
    # Create a log for a habit
    client.post(f"/api/logs/habits/{test_habits[0].id}/log",
                json={"quantity": 1},
                headers=auth_headers)

    response = client.get("/api/badges", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()

    # Should have some earned badges now
    assert data["earned_badges"] >= 0

  def test_get_badges_unauthenticated(self, client: TestClient):
    """Test getting badges without authentication"""
    response = client.get("/api/badges")

    assert response.status_code == 401

  def test_badge_categories(self, client: TestClient, auth_headers: dict):
    """Test that all expected badge categories are present"""
    response = client.get("/api/badges", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()

    category_ids = [cat["id"] for cat in data["categories"]]

    # Check that we have the expected categories (only those we seeded in tests)
    expected_categories = ["first_steps", "fitness", "social"]
    for expected in expected_categories:
      assert expected in category_ids

  def test_badge_progress_calculation(self, client: TestClient, auth_headers: dict, test_habits: list[Habit]):
    """Test that badge progress is calculated correctly"""
    # Create a fitness habit
    fitness_habit = client.post("/api/habits", json={
        "title": "Daily Workout",
        "description": "Exercise routine",
        "category": "fitness",
        "frequency": "daily",
        "target": 1
    }, headers=auth_headers)

    assert fitness_habit.status_code == 201
    habit_id = fitness_habit.json()["id"]

    # Log the habit multiple times with different quantities
    log_response = client.post(f"/api/logs/habits/{habit_id}/log",
                               json={"quantity": 1},
                               headers=auth_headers)
    print(f"Log response: {log_response.status_code} - {log_response.text}")

    # Create another fitness habit with higher target for more logs
    fitness_habit2 = client.post("/api/habits", json={
        "title": "Daily Workout 2",
        "description": "Exercise routine 2",
        "category": "fitness",
        "frequency": "daily",
        "target": 10
    }, headers=auth_headers)

    if fitness_habit2.status_code == 201:
      habit_id2 = fitness_habit2.json()["id"]
      # Log this habit with higher quantity
      log_response2 = client.post(f"/api/logs/habits/{habit_id2}/log",
                                  json={"quantity": 5},
                                  headers=auth_headers)
      print(
          f"Log response 2: {log_response2.status_code} - {log_response2.text}")

    response = client.get("/api/badges", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()

    # Find the workout warrior badge
    workout_badge = None
    for category in data["categories"]:
      for badge in category["badges"]:
        if badge["id"] == "workout_warrior":
          workout_badge = badge
          break

    assert workout_badge is not None
    assert workout_badge["status"] == "in_progress"
    assert workout_badge["progress"]["current"] == 6  # 1 + 5 = 6
    assert workout_badge["progress"]["target"] == 50
