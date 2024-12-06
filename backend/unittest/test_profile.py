# backend/unittest/test_profile.py
from .test_base import BaseTestCase

class TestProfileEndpoints(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.register_user("profileuser@example.com", "testpass", "Profile User")
        self.login_user("profileuser@example.com", "testpass")
    
    def test_update_profile(self):
        resp = self.client.post('/profile', json={"bio": "New bio", "name": "New Name"})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["success"], "Profile updated successfully")
        self.assertEqual(data["updated_profile"]["bio"], "New bio")

    def test_get_followings(self):
        resp = self.client.get('/profile')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("followings", data)
        self.assertIsInstance(data["followings"], list)

    def test_follow_unfollow(self):
        # Create another user to follow
        self.register_user("other@example.com", "testpass", "Other User")

        resp = self.client.post('/follow', json={"user_id": 2}) # 2 is the new user's ID if autoincrement from first user
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/unfollow', json={"user_id": 2})
        self.assertEqual(resp.status_code, 200)
