import pytest
from backend.database.create import User
from werkzeug.security import generate_password_hash


@pytest.fixture(autouse=True)
def patch_session(monkeypatch, db_session):
    # Ensure auth.py uses the test db_session
    monkeypatch.setattr("backend.auth.Session", lambda: db_session)
    monkeypatch.setattr(db_session, "close", lambda: None)

@pytest.mark.usefixtures("client", "db_session")
class TestAuth:
    def create_user_via_db(self, db_session, email, name, password):
        user = User(
            email=email,
            name=name,
            password_hash=generate_password_hash(password),
            username=email
        )
        db_session.add(user)
        db_session.commit()

    def test_signup_success(self, client):
        response = client.post('/signup', json={
            "email": "newuser@example.com",
            "password": "securepass",
            "name": "New User"
        })
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["success"] == "Yes"

    def test_signup_missing_fields(self, client):
        response = client.post('/signup', json={"email": "test@example.com"})
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data["reason"] == "Password is required"

    def test_signup_user_already_exists(self, client, db_session):
        self.create_user_via_db(db_session, "existing_user@example.com", "Existing User", "pass123")
        response_email = client.post('/signup', json={
            "email": "existing_user@example.com",
            "password": "pass123",
            "name": "New User"
        })
        assert response_email.status_code == 400
        json_data_email = response_email.get_json()
        assert json_data_email["reason"] == "User already exists with this username"

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
        self.create_user_via_db(db_session, "login_user@example.com", "Login User", "correctpass")
        response = client.post('/login', json={
            "email": "login_user@example.com",
            "password": "correctpass"
        })
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["success"] == "Yes"

    def test_ping_authenticated(self, client, db_session):
        self.create_user_via_db(db_session, "ping_user@example.com", "Ping User", "pass")
        client.post('/login', json={
            "email": "ping_user@example.com",
            "password": "pass"
        })
        response = client.get('/ping')
        json_data = response.get_json()
        assert response.status_code == 200
        assert json_data["authenticated"] is True

    def test_ping_unauthenticated(self, client):
        response = client.get('/ping')
        json_data = response.get_json()
        assert response.status_code == 200
        assert json_data["authenticated"] is False

    def test_logout_authenticated(self, client, db_session):
        self.create_user_via_db(db_session, "logout_user@example.com", "Logout User", "logoutpass")
        client.post('/login', json={
            "email": "logout_user@example.com",
            "password": "logoutpass"
        })
        response = client.get('/logout')
        assert response.status_code == 200

    def test_logout_unauthenticated(self, client):
        response = client.get('/logout')
        assert response.status_code == 401