import pytest
from backend.database.create import User

@pytest.fixture(autouse=True)
def patch_session(monkeypatch, db_session):
    """
    Monkeypatch the Session usage in auth.py to return the test db_session.
    Also patch the db_session.close method to do nothing to avoid detaching instances.
    This ensures that the session remains active and the test can safely query
    the database after routes return.
    """
    # Replace the Session call in auth.py with a lambda returning db_session
    monkeypatch.setattr("backend.auth.Session", lambda: db_session)
    # Prevent db_session from actually closing, which causes detached instances
    monkeypatch.setattr(db_session, "close", lambda: None)


@pytest.mark.usefixtures("client", "db_session")
class TestAuth:
    def create_user_via_client(self, client, email, password, name):
        """
        Helper function to create a user using the client.
        """
        response = client.post('/signup', json={
            "email": email,
            "password": password,
            "name": name
        })
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["success"] == "Yes"

    def login_user_via_client(self, client, email, password):
        """
        Helper function to log in a user using the client.
        """
        response = client.post('/login', json={
            "email": email,
            "password": password
        })
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["success"] == "Yes"

    def test_get_login_unauthorized(self, client):
        """
        Test that unauthenticated access to /login returns a proper response.
        """
        response = client.get('/login')
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data.get("Authorization") == "Unauthorized"

    def test_signup_missing_fields(self, client):
        """
        Test that signing up with missing fields returns an error.
        """
        response = client.post('/signup', json={"email": "test@example.com"})
        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data["reason"] == "Password is required"

    def test_signup_success(self, client):
        """
        Test that a new user can sign up successfully.
        """
        self.create_user_via_client(client, "newuser@example.com", "securepass", "New User")

    def test_signup_user_already_exists(self, client):
        """
        Test that signing up with an existing email returns an error.
        """
        self.create_user_via_client(client, "existing_user@example.com", "pass123", "Existing User")

        response = client.post('/signup', json={
            "email": "existing_user@example.com",
            "password": "pass123",
            "name": "Duplicate User"
        })

        assert response.status_code == 400
        json_data = response.get_json()
        assert json_data["reason"] == "Email already registered"

    def test_login_invalid_credentials(self, client):
        """
        Test that logging in with invalid credentials returns an error.
        """
        response = client.post('/login', json={
            "email": "nonexistent@example.com",
            "password": "wrongpass"
        })
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["success"] == "No"
        assert json_data["reason"] == "Invalid credentials"

    def test_login_success(self, client):
        """
        Test that a user can log in successfully.
        """
        self.create_user_via_client(client, "login_user@example.com", "correctpass", "Login User")
        self.login_user_via_client(client, "login_user@example.com", "correctpass")

    def test_ping_authenticated(self, client):
        """
        Test authenticated /ping endpoint.
        """
        self.create_user_via_client(client, "ping_user@example.com", "pass", "Ping User")
        self.login_user_via_client(client, "ping_user@example.com", "pass")

        response = client.get('/ping')
        json_data = response.get_json()
        assert response.status_code == 200
        assert json_data["authenticated"] is True

    def test_ping_unauthenticated(self, client):
        """
        Test unauthenticated /ping endpoint.
        """
        response = client.get('/ping')
        json_data = response.get_json()
        assert response.status_code == 200
        assert json_data["authenticated"] is False

    def test_logout_authenticated(self, client):
        """
        Test logout for an authenticated user.
        """
        self.create_user_via_client(client, "logout_user@example.com", "logoutpass", "Logout User")
        self.login_user_via_client(client, "logout_user@example.com", "logoutpass")

        response = client.get('/logout')
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data.get("message") == "Logged out successfully"

    def test_logout_unauthenticated(self, client):
        """
        Test logout for an unauthenticated user.
        """
        response = client.get('/logout')
        assert response.status_code == 401
