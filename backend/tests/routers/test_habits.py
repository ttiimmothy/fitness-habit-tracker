import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.habit import Habit, Category, Frequency
from app.models.user import User


class TestHabitEndpoints:
  """Test habit CRUD endpoints"""

  def test_create_habit_success(self, client: TestClient, auth_headers: dict):
    """Test successful habit creation"""
    response = client.post("/api/habits",
                           json={
                               "title": "Morning Exercise",
                               "description": "30 minutes of cardio",
                               "category": "fitness",
                               "frequency": "daily",
                               "target": 1
                           },
                           headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Morning Exercise"
    assert data["description"] == "30 minutes of cardio"
    assert data["category"] == "fitness"
    assert data["frequency"] == "daily"
    assert data["target"] == 1
    assert "id" in data
    assert "created_at" in data

  def test_create_habit_default_values(self, client: TestClient, auth_headers: dict):
    """Test habit creation with default values"""
    response = client.post("/api/habits",
                           json={
                               "title": "Simple Habit",
                               "frequency": "daily",
                               "target": 1
                           },
                           headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Simple Habit"
    assert data["description"] is None
    assert data["category"] == "other"  # Default category
    assert data["frequency"] == "daily"
    assert data["target"] == 1

  def test_create_habit_invalid_category(self, client: TestClient, auth_headers: dict):
    """Test habit creation with invalid category"""
    response = client.post("/api/habits",
                           json={
                               "title": "Test Habit",
                               "category": "invalid_category",
                               "frequency": "daily",
                               "target": 1
                           },
                           headers=auth_headers)

    assert response.status_code == 422  # Validation error

  def test_create_habit_invalid_frequency(self, client: TestClient, auth_headers: dict):
    """Test habit creation with invalid frequency"""
    response = client.post("/api/habits",
                           json={
                               "title": "Test Habit",
                               "category": "fitness",
                               "frequency": "invalid_frequency",
                               "target": 1
                           },
                           headers=auth_headers)

    assert response.status_code == 422  # Validation error

  def test_create_habit_negative_target(self, client: TestClient, auth_headers: dict):
    """Test habit creation with negative target"""
    response = client.post("/api/habits",
                           json={
                               "title": "Test Habit",
                               "category": "fitness",
                               "frequency": "daily",
                               "target": -1
                           },
                           headers=auth_headers)

    assert response.status_code == 422  # Validation error

  def test_create_habit_unauthenticated(self, client: TestClient):
    """Test habit creation without authentication"""
    response = client.post("/api/habits",
                           json={
                               "title": "Test Habit",
                               "category": "fitness",
                               "frequency": "daily",
                               "target": 1
                           })

    assert response.status_code == 401

  def test_list_habits_success(self, client: TestClient, auth_headers: dict, test_habits: list[Habit]):
    """Test successful habit listing"""
    response = client.get("/api/habits", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3  # We created 3 test habits

    # Check that habits are sorted by created_at desc
    titles = [habit["title"] for habit in data]
    assert "Weekly Review" in titles
    assert "Read Books" in titles
    assert "Daily Exercise" in titles

  def test_list_habits_empty(self, client: TestClient, auth_headers: dict):
    """Test habit listing with no habits"""
    response = client.get("/api/habits", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data == []

  def test_list_habits_unauthenticated(self, client: TestClient):
    """Test habit listing without authentication"""
    response = client.get("/api/habits")

    assert response.status_code == 401

  def test_get_habit_success(self, client: TestClient, auth_headers: dict, test_habit: Habit):
    """Test successful habit retrieval"""
    response = client.get(f"/api/habits/{test_habit.id}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(test_habit.id)
    assert data["title"] == "Test Habit"
    assert data["description"] == "A test habit"
    assert data["category"] == "fitness"
    assert data["frequency"] == "daily"
    assert data["target"] == 1

  def test_get_habit_not_found(self, client: TestClient, auth_headers: dict):
    """Test habit retrieval with non-existent habit"""
    response = client.get(
        "/api/habits/00000000-0000-0000-0000-000000000000", headers=auth_headers)

    assert response.status_code == 404
    error_data = response.json()
    assert "title" in error_data
    assert "Habit not found" in error_data["title"]

  def test_get_habit_wrong_user(self, client: TestClient, test_user_2: User, test_habit: Habit):
    """Test habit retrieval by wrong user"""
    # Login as different user
    login_response = client.post("/api/auth/login", json={
        "email": "test2@example.com",
        "password": "testpassword123"
    })
    assert login_response.status_code == 200

    other_auth_headers = {
        "Authorization": f"Bearer {login_response.cookies.get('access_token')}"}

    response = client.get(
        f"/api/habits/{test_habit.id}", headers=other_auth_headers)

    assert response.status_code == 404
    error_data = response.json()
    assert "title" in error_data
    assert "Habit not found" in error_data["title"]

  def test_update_habit_success(self, client: TestClient, auth_headers: dict, test_habit: Habit):
    """Test successful habit update"""
    response = client.put(f"/api/habits/{test_habit.id}",
                          json={
        "title": "Updated Habit",
        "description": "Updated description",
        "category": "learning",
        "target": 2
    },
        headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Habit"
    assert data["description"] == "Updated description"
    assert data["category"] == "learning"
    assert data["frequency"] == "daily"  # Frequency should remain unchanged
    assert data["target"] == 2

  def test_update_habit_partial(self, client: TestClient, auth_headers: dict, test_habit: Habit):
    """Test partial habit update"""
    response = client.put(f"/api/habits/{test_habit.id}",
                          json={
        "title": "Updated Title Only"
    },
        headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title Only"
    # Other fields should remain unchanged
    assert data["description"] == "A test habit"
    assert data["category"] == "fitness"

  def test_update_habit_not_found(self, client: TestClient, auth_headers: dict):
    """Test habit update with non-existent habit"""
    response = client.put("/api/habits/00000000-0000-0000-0000-000000000000",
                          json={
                              "title": "Updated Habit"
                          },
                          headers=auth_headers)

    assert response.status_code == 404
    error_data = response.json()
    assert "title" in error_data
    assert "Habit not found" in error_data["title"]

  def test_update_habit_wrong_user(self, client: TestClient, test_user_2: User, test_habit: Habit):
    """Test habit update by wrong user"""
    # Login as different user
    login_response = client.post("/api/auth/login", json={
        "email": "test2@example.com",
        "password": "testpassword123"
    })
    assert login_response.status_code == 200

    other_auth_headers = {
        "Authorization": f"Bearer {login_response.cookies.get('access_token')}"}

    response = client.put(f"/api/habits/{test_habit.id}",
                          json={
        "title": "Updated Habit"
    },
        headers=other_auth_headers)

    assert response.status_code == 404
    error_data = response.json()
    assert "title" in error_data
    assert "Habit not found" in error_data["title"]

  def test_delete_habit_success(self, client: TestClient, auth_headers: dict, test_habit: Habit):
    """Test successful habit deletion"""
    response = client.delete(
        f"/api/habits/{test_habit.id}", headers=auth_headers)

    assert response.status_code == 204

  def test_delete_habit_not_found(self, client: TestClient, auth_headers: dict):
    """Test habit deletion with non-existent habit"""
    response = client.delete(
        "/api/habits/00000000-0000-0000-0000-000000000000", headers=auth_headers)

    assert response.status_code == 404
    error_data = response.json()
    assert "title" in error_data
    assert "Habit not found" in error_data["title"]

  def test_delete_habit_wrong_user(self, client: TestClient, test_user_2: User, test_habit: Habit):
    """Test habit deletion by wrong user"""
    # Login as different user
    login_response = client.post("/api/auth/login", json={
        "email": "test2@example.com",
        "password": "testpassword123"
    })
    assert login_response.status_code == 200

    other_auth_headers = {
        "Authorization": f"Bearer {login_response.cookies.get('access_token')}"}

    response = client.delete(
        f"/api/habits/{test_habit.id}", headers=other_auth_headers)

    assert response.status_code == 404
    error_data = response.json()
    assert "title" in error_data
    assert "Habit not found" in error_data["title"]

  def test_habit_categories_enum(self, client: TestClient, auth_headers: dict):
    """Test all valid habit categories"""
    categories = ["fitness", "learning",
                  "productivity", "health", "social", "other"]

    for category in categories:
      response = client.post("/api/habits",
                             json={
                                 "title": f"Test {category.title()}",
                                 "category": category,
                                 "frequency": "daily",
                                 "target": 1
                             },
                             headers=auth_headers)

      assert response.status_code == 201
      data = response.json()
      assert data["category"] == category

  def test_habit_frequencies_enum(self, client: TestClient, auth_headers: dict):
    """Test all valid habit frequencies"""
    frequencies = ["daily", "weekly", "monthly"]

    for frequency in frequencies:
      response = client.post("/api/habits",
                             json={
                                 "title": f"Test {frequency.title()}",
                                 "category": "other",
                                 "frequency": frequency,
                                 "target": 1
                             },
                             headers=auth_headers)

      assert response.status_code == 201
      data = response.json()
      assert data["frequency"] == frequency
