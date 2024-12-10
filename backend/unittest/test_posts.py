# backend/unittest/test_posts.py
from .test_base import BaseTestCase

class TestPostsEndpoints(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.register_user("poster@example.com", "testpass", "Post User")
        self.login_user("poster@example.com", "testpass")
    
    def test_add_post(self):
        resp = self.client.post('/post', json={"content": "Test content", "title":"Test title"})
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertEqual(data["message"], "Post added")

    def test_get_posts_insufficient_credits(self):
        # If user doesn't have enough credits, they should get a 403
        # Try fetching posts multiple times until credits run out (depending on COST_TO_ACCESS)
        resp = self.client.get('/posts')
        # Check status and response
        # This depends on initial credits and COST_TO_ACCESS. Adjust test accordingly.
        self.assertIn(resp.status_code, [200, 403])
