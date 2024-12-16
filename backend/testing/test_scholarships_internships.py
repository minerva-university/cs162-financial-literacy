"""from .test_base import BaseTestCase
from datetime import datetime, timedelta, timezone
from ..database.create import ListingStatus, Scholarship, Internship, User  # Import User


class TestScholarshipsInternshipsEndpoints(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Register and log in a test user
        resp = self.register_user("testuser@example.com", "testpassword", "Test User")
        self.assertEqual(resp.status_code, 200, f"Failed to register user. Response: {resp.get_json()}")

        # Fetch the test user directly
        self.test_user = self.session.query(User).filter_by(email="testuser@example.com").first()
        self.assertIsNotNone(self.test_user, "Test user not created properly.")

        # Log in as the test user
        self.login_user("testuser@example.com", "testpassword")

    def test_post_scholarship(self):
        payload = {
            "title": "Test Scholarship",
            "description": "A test scholarship",
            "amount": 1000,
            "application_link": "http://example.com",
            "deadline": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
            "status": ListingStatus.ACTIVE.value,
        }

        resp = self.client.post("/scholarships", json=payload)
        self.assertEqual(resp.status_code, 201, f"Unexpected status code: {resp.status_code}. Response: {resp.get_json()}")
        data = resp.get_json()
        self.assertIn("scholarship_id", data, "Response does not contain scholarship_id.")

    def test_get_scholarships(self):
        scholarship = Scholarship(
            user_id=self.test_user.user_id,
            title="Another Scholarship",
            description="Description",
            amount=1500,
            application_link="http://example2.com",
            deadline=datetime.now(timezone.utc) + timedelta(days=30),
            status=ListingStatus.ACTIVE,
        )
        self.session.add(scholarship)
        self.session.commit()

        resp = self.client.get("/scholarships")
        self.assertEqual(resp.status_code, 200, f"Unexpected status code: {resp.status_code}. Response: {resp.get_json()}")
        data = resp.get_json()
        self.assertIsInstance(data, list, "Response should be a list.")
        self.assertGreaterEqual(len(data), 1, "No scholarships found.")

    def test_post_internship(self):
        payload = {
            "title": "Test Internship",
            "description": "A test internship",
            "requirements": "Some requirements",
            "application_link": "http://example.com",
            "deadline": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
            "status": ListingStatus.ACTIVE.value,
        }

        resp = self.client.post("/internships", json=payload)
        self.assertEqual(resp.status_code, 201, f"Unexpected status code: {resp.status_code}. Response: {resp.get_json()}")
        data = resp.get_json()
        self.assertIn("internship_id", data, "Response does not contain internship_id.")
"""