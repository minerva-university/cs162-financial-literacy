# test_posts.py

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

    def test_add_post_success(self, client, create_user, login_user):
        user = create_user(username="post_user", email="post_user@example.com", password="pass", credits=100)
        login_user(email="post_user@example.com", password="pass")

        response = client.post('/post', json={
            "title": "Test Post",
            "content": "This is a test post."
        })

        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data["message"] == "Post added"
        assert json_data["post"]["id"] is not None


    def test_get_posts_with_insufficient_credits(self, client, create_user, login_user):
        # Create and log in a user with 0 credits
        user = create_user(username="low_credits_user", email="low@example.com", password="pass", credits=0)
        login_user(email="low@example.com", password="pass")
        
        response = client.get('/posts')
        assert response.status_code == 403
        json_data = response.get_json()
        assert json_data["error"] == "Insufficient credits"

    def test_get_posts_success(self, client, create_user, login_user, db_session):
        # Clear existing posts first
        db_session.query(Post).delete()
        db_session.commit()

        user = create_user(username="rich_user", email="rich_user@example.com", password="pass", credits=100)
        post = Post(user_id=user.user_id, title="Test Post", content="Test Content")
        db_session.add(post)
        db_session.commit()

        login_user(email="rich_user@example.com", password="pass")

        response = client.get('/posts')
        json_data = response.get_json()

        assert response.status_code == 200



    def test_fetch_single_post(self, client, create_user, login_user, db_session):
        # Create a user and a post
        user = create_user(username="fetch_user", email="fetch@example.com", password="pass", credits=100)
        post = Post(user_id=user.user_id, title="Fetch Title", content="Fetch Content")
        db_session.add(post)
        db_session.commit()

        # Log in and fetch the post
        login_user(email="fetch@example.com", password="pass")
        response = client.get(f'/post/{post.post_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data["post"]["title"] == "Fetch Title"

    def test_delete_own_post(self, client, create_user, login_user, db_session):
        # Create a user and a post
        user = create_user(username="del_user", email="del@example.com", password="pass")
        post = Post(user_id=user.user_id, title="To Delete", content="Delete me")
        db_session.add(post)
        db_session.commit()

        # Log in and delete the post
        login_user(email="del@example.com", password="pass")
        response = client.delete(f'/post/{post.post_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data["message"] == "Post deleted successfully"

        # Verify post is deleted
        deleted_post = db_session.query(Post).filter_by(post_id=post.post_id).first()
        assert deleted_post is None

    def test_delete_other_users_post(self, client, create_user, login_user, db_session):
        # Create two users and a post
        user1 = create_user(username="u1", email="u1@example.com", password="pass")
        user2 = create_user(username="u2", email="u2@example.com", password="pass")
        post = Post(user_id=user1.user_id, title="User1 Post", content="Content")
        db_session.add(post)
        db_session.commit()

        # Log in as user2 and try to delete user1's post
        login_user(email="u2@example.com", password="pass")
        response = client.delete(f'/post/{post.post_id}')
        assert response.status_code == 403
        json_data = response.get_json()
        assert json_data["error"] == "Unauthorized: You can only delete your own posts"

    def test_vote_on_post(self, client, create_user, login_user, db_session):
        # Create a user and a post
        user = create_user(username="voter", email="voter@example.com", password="pass")
        post = Post(user_id=user.user_id, title="Vote Post", content="Votable")
        db_session.add(post)
        db_session.commit()

        # Log in and vote on the post
        login_user(email="voter@example.com", password="pass")
        response = client.post(f'/post/{post.post_id}/vote', json={"vote_type": "upvote"})
        assert response.status_code == 200
        data = response.get_json()
        assert "Vote" in data["message"]

    def test_comment_on_post(self, client, create_user, login_user, db_session):
        # Create a user and a post
        user = create_user(username="commenter", email="commenter@example.com", password="pass")
        post = Post(user_id=user.user_id, title="Comment Post", content="Comment here")
        db_session.add(post)
        db_session.commit()

        # Log in and comment on the post
        login_user(email="commenter@example.com", password="pass")
        response = client.post(f'/post/{post.post_id}/comment', json={"comment_text": "Nice post!"})
        assert response.status_code == 201
        data = response.get_json()
        assert "Comment added successfully" in data["message"]

        # Verify comment exists in the database
        comment = db_session.query(Comment).filter_by(post_id=post.post_id).first()
        assert comment is not None
        assert comment.comment_text == "Nice post!"
