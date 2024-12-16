# test_profile.py
# Same reasoning as test_posts.py: we no longer need to patch Session directly since app.session_factory is set.
import pytest
from backend.database.create import User, Follow

@pytest.mark.usefixtures("client", "db_session")
class TestProfile:
    """
    Test cases for the profile-related endpoints.
    Ensures that users can update profiles, retrieve followings,
    view others' profiles, and follow/unfollow users correctly.
    """

    @pytest.fixture(autouse=True)
    def clean_db_before_each_test(self, db_session):
        """
        Clean the database before each test to ensure no leftover data.
        """
        db_session.query(Follow).delete()
        db_session.query(User).delete()
        db_session.commit()

    def test_get_own_profile_unauthenticated(self, client):
        response = client.get('/profile')
        assert response.status_code == 401, "Expected status code 401 for unauthenticated access."

    def test_update_profile(self, client, create_user, login_user, db_session):
        user = create_user(
            username="profile_user",
            email="profile_user@example.com",
            password="pass",
            name="Original Name"
        )
        login_user(email="profile_user@example.com", password="pass")

        response = client.post('/profile', json={
            "bio": "This is my new bio",
            "name": "Profile User Updated"
        })
        json_data = response.get_json()

        assert response.status_code == 200, "Expected status code 200 for successful profile update."
        assert json_data["updated_profile"]["bio"] == "This is my new bio"
        assert json_data["updated_profile"]["name"] == "Profile User Updated"

    def test_get_followings(self, client, create_user, login_user, db_session):
        main_user = create_user(
            username="main_user",
            email="main_user@example.com",
            password="pass",
            name="Main User"
        )
        followed_user = create_user(
            username="followed_user",
            email="followed_user@example.com",
            password="pass",
            name="followed_user"
        )
        db_session.commit()

        follow = Follow(
            follower_id=main_user.user_id,
            followed_id=followed_user.user_id
        )
        db_session.add(follow)
        db_session.commit()

        login_user(email="main_user@example.com", password="pass")

        response = client.get('/profile')
        assert response.status_code == 200, "Expected status code 200 when retrieving followings."
        json_data = response.get_json()
        assert "followed_user" in json_data["followings"], (
            f"Expected 'followed_user' in followings, got {json_data['followings']}"
        )

    def test_get_others_profile(self, client, create_user, login_user, db_session):
        other_user = create_user(
            username="other_user",
            email="other_user@example.com",
            password="pass",
            name="other_user"
        )
        main_user = create_user(
            username="main_user",
            email="main_user@example.com",
            password="pass",
            name="Main User"
        )
        db_session.commit()

        login_user(email="main_user@example.com", password="pass")

        response = client.get(f'/profile/{other_user.user_id}')
        assert response.status_code == 200, "Expected status code 200 when retrieving another user's profile."
        json_data = response.get_json()
        assert json_data["name"] == "other_user", (
            f"Expected name 'other_user', got '{json_data['name']}'"
        )

    def test_follow_unfollow(self, client, create_user, login_user, db_session):
        user = create_user(
            username="user_a",
            email="user_a@example.com",
            password="pass",
            name="User A"
        )
        target = create_user(
            username="user_b",
            email="user_b@example.com",
            password="pass",
            name="User B"
        )
        db_session.commit()

        login_user(email="user_a@example.com", password="pass")

        # Follow user_b
        res = client.post('/follow', json={"user_id": target.user_id})
        assert res.status_code == 200, (
            f"Expected status code 200 when following. Got {res.status_code}"
        )
        data = res.get_json()
        assert data["success"] == "Successfully followed user", f"Got '{data.get('success')}' instead of success message"

        # Verify the follow relationship in DB
        follow = db_session.query(Follow).filter_by(
            follower_id=user.user_id,
            followed_id=target.user_id
        ).first()
        assert follow is not None, "Follow relationship not created."

        # Unfollow user_b
        res = client.post('/unfollow', json={"user_id": target.user_id})
        assert res.status_code == 200, "Expected status code 200 when unfollowing."
        data = res.get_json()
        assert data["success"] == "Successfully unfollowed user", f"Expected unfollow success message, got {data}"

        # Confirm the follow relationship no longer exists
        follow = db_session.query(Follow).filter_by(
            follower_id=user.user_id,
            followed_id=target.user_id
        ).first()
        assert follow is None, "Follow relationship was not removed."