# backend/unittest/test_auth.py
from .test_base import BaseTestCase
from datetime import datetime

class TestAuthEndpoints(BaseTestCase):
    def test_signup_success(self):
        email = f"test_user_{datetime.now().timestamp()}@example.com"
        resp = self.register_user(email=email, password="testpass", name="Tester")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["success"], "Yes")

    def test_signup_missing_password(self):
        resp = self.client.post('/signup', json={"email":"test2@example.com"})
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertEqual(data["success"], "No")

    def test_login_success(self):
        # First sign up
        self.register_user("login@example.com", "testpass")
        # Then login
        resp = self.login_user("login@example.com", "testpass")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["success"], "Yes")

    def test_login_invalid_credentials(self):
        resp = self.login_user("notexist@example.com", "wrongpass")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["success"], "No")

    def test_logout(self):
        # Login user
        self.register_user("logout@example.com", "testpass")
        self.login_user("logout@example.com", "testpass")
        resp = self.logout_user()
        self.assertEqual(resp.status_code, 200)
