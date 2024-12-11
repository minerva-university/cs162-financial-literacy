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

    def test_signup_user_already_exists(self, client, db_session):
        client.post('/signup', json={
            "email": "existing_user@example.com",
            "password": "pass123",
            "name": "Existing User"
        })
        response = client.post('/signup', json={
            "email": "existing_user@example.com",
            "password": "pass123",
            "name": "Duplicate User"
        })
        json_data = response.get_json()
        assert json_data["success"] == "No"
        assert "User already exists" in json_data["reason"]



    def test_login_invalid_credentials(self, client):
        response = client.post('/login', json={
            "email": "nonexistent@example.com",
            "password": "wrongpass"
        })
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["success"] == "No"
        assert json_data["reason"] == "Invalid credentials"

    def test_login_success(self, client, db_session):
        user = User(username="login_user", email="login_user@example.com")
        user.set_password("correctpass")
        db_session.add(user)
        db_session.commit()

        response = client.post('/login', json={
            "email": "login_user@example.com",
            "password": "correctpass"
        })
        json_data = response.get_json()
        assert json_data["success"] == "Yes"

    def test_ping_authenticated(client, db_session):
        user = User(username="ping_user", email="ping_user@example.com", password_hash="hashed_password")
        db_session.add(user)
        db_session.commit()

        # Log in the user
        client.post('/login', json={"email": "ping_user@example.com", "password": "hashed_password"})

        # Test /ping endpoint
        response = client.get('/ping')
        json_data = response.get_json()
        assert json_data["authenticated"] is True
        assert json_data["username"] == "ping_user"


    def test_ping_unauthenticated(self, client):
        response = client.get('/ping')
        json_data = response.get_json()
        assert json_data["authenticated"] is False

    def test_logout_authenticated(self, client, db_session):
        user = User(username="logout_user", email="logout_user@example.com")
        user.set_password("logoutpass")
        db_session.add(user)
        db_session.commit()

        client.post('/login', json={
            "email": "logout_user@example.com",
            "password": "logoutpass"
        })
        response = client.get('/logout')
        assert response.status_code == 200

    def test_logout_unauthenticated(self, client):
        response = client.get('/logout')
        assert response.status_code == 401

    def test_get_available_mentors(self, client, db_session):
        mentor1 = User(username="mentor1", email="mentor1@example.com", mentorship_availability=True)
        mentor1.set_password("pass")
        mentor2 = User(username="mentor2", email="mentor2@example.com", mentorship_availability=True)
        mentor2.set_password("pass")
        db_session.add_all([mentor1, mentor2])
        db_session.commit()

        response = client.get('/mentors/available')
        json_data = response.get_json()
        assert len(json_data["mentors"]) == 2
