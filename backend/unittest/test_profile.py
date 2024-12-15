import pytest
from backend.database.create import User, Follow

@pytest.mark.usefixtures("client", "db_session")
class TestProfile:
    def test_get_own_profile_unauthenticated(self, client):
        response = client.get('/profile')
        # Should return 401 because login_required
        assert response.status_code == 401

    def test_update_profile(self, client, create_user, login_user):
        # Create a user and log them in
        user = create_user(username="profile_user", email="profile_user@example.com", password="pass")
        login_user(email="profile_user@example.com", password="pass")

        # Update the profile
        response = client.post('/profile', json={
            "bio": "This is my new bio",
            "name": "Profile User Updated"
        })
        json_data = response.get_json()
        assert response.status_code == 200
        assert json_data["updated_profile"]["bio"] == "This is my new bio"
        assert json_data["updated_profile"]["name"] == "Profile User Updated"

    def test_get_followings(self, client, create_user, login_user, db_session):
        # Create main_user and followed_user
        main_user = create_user(username="main_user", email="main_user@example.com", password="pass")
        followed_user = create_user(username="followed_user", email="followed_user@example.com", password="pass")

        # Create follow relationship
        follow = Follow(follower_id=main_user.user_id, followed_id=followed_user.user_id)
        db_session.add(follow)
        db_session.commit()

        login_user(email="main_user@example.com", password="pass")

        # The code defines followings on GET /profile, not /profile/followings
        response = client.get('/profile')
        assert response.status_code == 200
        json_data = response.get_json()
        # The code returns a list of strings (names), not dicts with 'name' keys
        # Just check that "followed_user" is in that list
        assert "followed_user" in json_data["followings"]

    def test_get_others_profile(self, client, create_user, login_user):
        # Create other_user with a name that matches the username
        other_user = create_user(username="other_user", email="other_user@example.com", password="pass", name="other_user")
        main_user = create_user(username="main_user", email="main_user@example.com", password="pass")

        # Log in as the main user
        login_user(email="main_user@example.com", password="pass")

        # Fetch the other user's profile
        response = client.get(f'/profile/{other_user.user_id}')
        json_data = response.get_json()
        assert response.status_code == 200
        # Now that we set name="other_user", it should match
        assert json_data["name"] == "other_user"

    def test_follow_unfollow(self, client, create_user, login_user, db_session):
        # Ensure a clean state by removing any existing follow relationships
        db_session.query(Follow).delete()
        db_session.commit()

        # Create two distinct users
        user = create_user(username="user_a", email="user_a@example.com", password="pass")
        target = create_user(username="user_b", email="user_b@example.com", password="pass")

        # Log in as user_a
        login_user(email="user_a@example.com", password="pass")

        # Follow user_b
        res = client.post('/follow', json={"user_id": target.user_id})
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] == "Successfully followed user"

        # Check the follow relationship exists
        follow = db_session.query(Follow).filter_by(follower_id=user.user_id, followed_id=target.user_id).first()
        assert follow is not None

        # Unfollow user_b
        res = client.post('/unfollow', json={"user_id": target.user_id})
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] == "Successfully unfollowed user"

        # Check the follow relationship no longer exists
        follow = db_session.query(Follow).filter_by(follower_id=user.user_id, followed_id=target.user_id).first()
        assert follow is None
