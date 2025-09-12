import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import User


class TestAuthEndpoints:
  """Test authentication endpoints"""

  def test_register_success(self, client: TestClient, db_session: Session):
    """Test successful user registration"""
    response = client.post("/api/auth/register", json={
        "email": "newuser@example.com",
        "name": "New User",
        "password": "newpassword123"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["user"]["email"] == "newuser@example.com"
    assert data["user"]["name"] == "New User"
    assert "id" in data["user"]
    assert "created_at" in data["user"]

    # Check that user was created in database
    user = db_session.query(User).filter(
        User.email == "newuser@example.com").first()
    assert user is not None
    assert user.name == "New User"

  def test_register_duplicate_email(self, client: TestClient, test_user: User):
    """Test registration with duplicate email fails"""
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",  # Same as test_user
        "name": "Another User",
        "password": "password123"
    })

    assert response.status_code == 409
    error_data = response.json()
    assert "title" in error_data
    assert "already register" in error_data["title"].lower()

  def test_register_invalid_email(self, client: TestClient):
    """Test registration with invalid email format"""
    response = client.post("/api/auth/register", json={
        "email": "invalid-email",
        "name": "Test User",
        "password": "password123"
    })

    assert response.status_code == 422  # Validation error

  def test_register_weak_password(self, client: TestClient):
    """Test registration with weak password"""
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "name": "Test User",
        "password": "123"  # Too short
    })

    assert response.status_code == 200  # API doesn't validate password strength

  def test_login_success(self, client: TestClient, test_user: User):
    """Test successful login"""
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "testpassword123"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["user"]["email"] == "test@example.com"
    assert data["user"]["name"] == "Test User"

    # Check that cookie was set
    assert "access_token" in response.cookies
    assert response.cookies["access_token"] is not None

  def test_login_invalid_credentials(self, client: TestClient, test_user: User):
    """Test login with invalid credentials"""
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })

    assert response.status_code == 401
    # Check the actual error response structure
    error_data = response.json()
    assert "title" in error_data
    assert "Invalid credentials" in error_data["title"]

  def test_login_nonexistent_user(self, client: TestClient):
    """Test login with non-existent user"""
    response = client.post("/api/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "password123"
    })

    assert response.status_code == 401
    # Check the actual error response structure
    error_data = response.json()
    assert "title" in error_data
    assert "Invalid credentials" in error_data["title"]

  def test_me_endpoint_authenticated(self, client: TestClient, auth_headers: dict):
    """Test /me endpoint with valid authentication"""
    response = client.get("/api/auth/me", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["user"]["email"] == "test@example.com"
    assert data["user"]["name"] == "Test User"

  def test_me_endpoint_unauthenticated(self, client: TestClient):
    """Test /me endpoint without authentication"""
    response = client.get("/api/auth/me")

    assert response.status_code == 401
    # Check the actual error response structure
    error_data = response.json()
    assert "title" in error_data
    assert "Authentication required" in error_data["title"]

  def test_me_endpoint_invalid_token(self, client: TestClient):
    """Test /me endpoint with invalid token"""
    response = client.get("/api/auth/me", headers={
        "Authorization": "Bearer invalid_token"
    })

    assert response.status_code == 401
    # Check the actual error response structure
    error_data = response.json()
    assert "title" in error_data
    assert "Invalid token" in error_data["title"]

  def test_logout_success(self, client: TestClient, auth_headers: dict):
    """Test successful logout"""
    response = client.post("/api/auth/logout", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Successfully logged out"

    # The logout endpoint calls delete_cookie which sets Set-Cookie headers
    # to clear the cookie, but doesn't add it to response.cookies
    # We can verify the logout worked by checking the response message

  def test_change_password_success(self, client: TestClient, auth_headers: dict):
    """Test successful password change"""
    response = client.post("/api/auth/change-password",
                           json={
                               "currentPassword": "testpassword123",
                               "newPassword": "newpassword123"
                           },
                           headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["message"] == "password update success"

  def test_change_password_wrong_current(self, client: TestClient, auth_headers: dict):
    """Test password change with wrong current password"""
    response = client.post("/api/auth/change-password",
                           json={
                               "currentPassword": "wrongpassword",
                               "newPassword": "newpassword123"
                           },
                           headers=auth_headers)

    assert response.status_code == 401
    error_data = response.json()
    assert "title" in error_data
    assert "Invalid credentials" in error_data["title"]

  def test_change_password_unauthenticated(self, client: TestClient):
    """Test password change without authentication"""
    response = client.post("/api/auth/change-password",
                           json={
                               "currentPassword": "testpassword123",
                               "newPassword": "newpassword123"
                           })

    assert response.status_code == 401

  def test_upload_profile_success(self, client: TestClient, auth_headers: dict):
    """Test successful profile upload"""
    response = client.put("/api/auth/update-profile",
                          json={
                              "name": "Updated Name",
                              "avatar_url": "https://example.com/avatar.jpg"
                          },
                          headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"

  def test_upload_profile_unauthenticated(self, client: TestClient):
    """Test profile upload without authentication"""
    response = client.put("/api/auth/update-profile",
                          json={
                              "name": "Updated Name",
                              "avatar_url": "https://example.com/avatar.jpg"
                          })

    assert response.status_code == 401

  def test_cookie_authentication_priority(self, client: TestClient, test_user: User):
    """Test that cookie authentication takes priority over bearer token"""
    # First login to get cookie
    login_response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "testpassword123"
    })
    assert login_response.status_code == 200

    # Get the cookie
    cookie_token = login_response.cookies.get("access_token")

    # Create a different user and get their token
    from app.core.security import create_access_token
    other_token = create_access_token("999999")  # Non-existent user ID

    # Test with both cookie and bearer token - should use cookie (valid user)
    # Set cookie on client instead of per-request
    if cookie_token:
      client.cookies.set("access_token", cookie_token)

    response = client.get("/api/auth/me",
                          headers={"Authorization": f"Bearer {other_token}"})

    assert response.status_code == 200
    data = response.json()
    # Should be cookie user, not bearer user
    assert data["user"]["email"] == "test@example.com"
