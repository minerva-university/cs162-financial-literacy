# tests/test_posts.py
import pytest
from backend.database.create import User, Post, Vote, Comment
from backend.config import COST_TO_ACCESS, REWARD_FOR_POSTING

@pytest.mark.usefixtures("client", "db_session")
class TestPosts:
    def test_add_post_unauthenticated(self, client):
        response = client.post('/post', json={
            "title": "My Post",
            "content": "Post content"
        })
        assert response.status_code == 401

    def test_add_post_success(self, client, db_session):
        user = User(username="post_user", email="post_user@example.com", credits=100)
        user.set_password("pass")
        db_session.add(user)
        db_session.commit()

        client.post('/login', json={
            "email": "post_user@example.com",
            "password": "pass"
        })

        response = client.post('/post', json={
            "title": "Test Post",
            "content": "This is a test post."
        })

        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data["message"] == "Post added"



    def test_get_posts_with_insufficient_credits(self, client, db_session):
        user = User(username="low_credits_user", email="low@example.com", credits=0)
        user.set_password("pass")
        db_session.add(user)
        db_session.commit()

        client.post('/login', json={
            "email": "low@example.com",
            "password": "pass"
        })

        res = client.get('/posts')
        assert res.status_code == 403

    def test_get_posts_success(self, client, db_session):
        user = User(username="rich_user", email="rich@example.com", credits=100)
        user.set_password("pass")
        db_session.add(user)
        post = Post(user_id=user.user_id, title="Test Post", content="Test Content")
        db_session.add(post)
        db_session.commit()

        client.post('/login', json={
            "email": "rich@example.com",
            "password": "pass"
        })

        res = client.get('/posts')
        data = res.get_json()
        assert res.status_code == 200
        assert len(data["posts"]) == 1

        db_session.refresh(user)
        # User should have COST_TO_ACCESS deducted
        assert user.credits == 100 - COST_TO_ACCESS

    def test_fetch_single_post(self, client, db_session):
        user = User(username="fetch_user", email="fetch@example.com", credits=100)
        user.set_password("pass")
        db_session.add(user)
        post = Post(user_id=user.user_id, title="Fetch Title", content="Fetch Content")
        db_session.add(post)
        db_session.commit()

        client.post('/login', json={
            "email": "fetch@example.com",
            "password": "pass"
        })

        res = client.get(f'/post/{post.post_id}')
        assert res.status_code == 200
        data = res.get_json()
        assert data["post"]["title"] == "Fetch Title"

    def test_delete_own_post(self, client, db_session):
        user = User(username="del_user", email="del@example.com", credits=100)
        user.set_password("pass")
        db_session.add(user)
        db_session.commit()

        post = Post(user_id=user.user_id, title="To Delete", content="Delete me")
        db_session.add(post)
        db_session.commit()

        client.post('/login', json={
            "email": "del@example.com",
            "password": "pass"
        })

        res = client.delete(f'/post/{post.post_id}')
        assert res.status_code == 200
        data = res.get_json()
        assert data["message"] == "Post deleted successfully"

    def test_delete_other_users_post(self, client, db_session):
        user1 = User(username="u1", email="u1@example.com", credits=100)
        user1.set_password("pass")
        user2 = User(username="u2", email="u2@example.com", credits=100)
        user2.set_password("pass")
        db_session.add_all([user1, user2])
        db_session.commit()

        post = Post(user_id=user1.user_id, title="User1 Post", content="Content")
        db_session.add(post)
        db_session.commit()

        # Login as user2
        client.post('/login', json={
            "email": "u2@example.com",
            "password": "pass"
        })

        res = client.delete(f'/post/{post.post_id}')
        assert res.status_code == 403

    def test_vote_on_post(self, client, db_session):
        user = User(username="voter", email="voter@example.com", credits=100)
        user.set_password("pass")
        db_session.add(user)
        db_session.commit()

        post = Post(user_id=user.user_id, title="Vote Post", content="Votable")
        db_session.add(post)
        db_session.commit()

        client.post('/login', json={
            "email": "voter@example.com",
            "password": "pass"
        })

        res = client.post(f'/post/{post.post_id}/vote', json={"vote_type": "upvote"})
        assert res.status_code == 200
        data = res.get_json()
        assert "Vote added" in data["message"]

        # Remove vote
        res = client.delete(f'/post/{post.post_id}/vote')
        assert res.status_code == 200
        data = res.get_json()
        assert "Vote deleted successfully" in data["message"]

    def test_comment_on_post(self, client, db_session):
        user = User(username="commenter", email="commenter@example.com", credits=100)
        user.set_password("pass")
        db_session.add(user)
        db_session.commit()

        post = Post(user_id=user.user_id, title="Comment Post", content="Comment here")
        db_session.add(post)
        db_session.commit()

        client.post('/login', json={
            "email": "commenter@example.com",
            "password": "pass"
        })

        res = client.post(f'/post/{post.post_id}/comment', json={"comment_text": "Nice post!"})
        assert res.status_code == 201
        data = res.get_json()
        assert "Comment added successfully" in data["message"]
