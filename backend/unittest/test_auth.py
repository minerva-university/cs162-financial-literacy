# test_auth.py

import pytest
from backend.database.create import User

@pytest.mark.usefixtures("client", "db_session")
class TestAuth:
    def test_get_login_unauthorized(self, client):
        response = client.get('/login')
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data.get("Authorization") == "Unauthorized"

    def test_signup_missing_fields(self, client):
        response = client.post('/signup', json={"email": "test@example.com"})
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data["reason"] == "Password is required"

    def test_signup_success(self, client, db_session):
        response = client.post('/signup', json={
            "email": "newuser@example.com",
            "password": "securepass",
            "name": "New User"
        })
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["success"] == "Yes"
        user = db_session.query(User).filter_by(email="newuser@example.com").first()
        assert user is not None

    def test_signup_user_already_exists(self, client, db_session, create_user):
        # Use create_user fixture to set up initial user
        create_user(username="existing_user", email="existing_user@example.com", password="pass123")

        response = client.post('/signup', json={
            "email": "existing_user@example.com",
            "password": "pass123",
            "name": "Duplicate User"
        })

        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data["reason"] == "Email already registered"


    def test_login_invalid_credentials(self, client):
        response = client.post('/login', json={
            "email": "nonexistent@example.com",
            "password": "wrongpass"
        })
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["success"] == "No"
        assert json_data["reason"] == "Invalid credentials"

    def test_login_success(self, client, create_user, login_user):
        create_user(username="login_user", email="login_user@example.com", password="correctpass")
        response = login_user(email="login_user@example.com", password="correctpass")
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["success"] == "Yes"

    def test_ping_authenticated(self, client, create_user, login_user):
        user = create_user(username="ping_user", email="ping_user@example.com", password="pass")
        login_user(email="ping_user@example.com", password="pass")

        response = client.get('/ping')
        json_data = response.get_json()
        assert response.status_code == 200
        assert json_data["authenticated"] is True

    def test_ping_unauthenticated(self, client):
        response = client.get('/ping')
        json_data = response.get_json()
        assert response.status_code == 200
        assert json_data["authenticated"] is False

    def test_logout_authenticated(self, client, create_user, login_user):
        create_user(username="logout_user", email="logout_user@example.com", password="logoutpass")
        login_user(email="logout_user@example.com", password="logoutpass")
        response = client.get('/logout')
        assert response.status_code == 200

    def test_logout_unauthenticated(self, client):
        response = client.get('/logout')
        assert response.status_code == 401