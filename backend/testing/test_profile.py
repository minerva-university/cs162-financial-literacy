# test_profile.py
import pytest
from backend.database.create import User, Follow

@pytest.fixture(autouse=True)
def patch_profile_session(monkeypatch, db_session):
    """
    Monkeypatch the Session and engine in profile.py to use the test db_session.
    This ensures that profile.py uses the same database session as the tests,
    allowing data created in tests to be visible to profile.py routes.
    
    Additionally, prevent db_session from closing to avoid DetachedInstanceError
    when accessing objects after route handlers run.
    """
    # Patch the engine in backend.database.create to use the test session's bind
    monkeypatch.setattr("backend.database.create.engine", db_session.bind)
    
    # Patch the Session in profile.py to return the test db_session
    monkeypatch.setattr("backend.profile.Session", lambda: db_session)
    
    # Prevent db_session.close() from detaching instances during tests
    monkeypatch.setattr(db_session, "close", lambda: None)

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
        Clean the database before each test to ensure no leftover data
        affects the test outcomes.
        """
        db_session.query(Follow).delete()
        db_session.query(User).delete()
        db_session.commit()

    def test_get_own_profile_unauthenticated(self, client):
        """
        Test that accessing the own profile without authentication
        returns a 401 Unauthorized status.
        """
        response = client.get('/profile')
        assert response.status_code == 401, "Expected status code 401 for unauthenticated access."

    def test_update_profile(self, client, create_user, login_user, db_session):
        """
        Test that a logged-in user can successfully update their profile.
        """
        # Create and log in a user with an initial name
        user = create_user(
            username="profile_user",
            email="profile_user@example.com",
            password="pass",
            name="Original Name"
        )
        login_user(email="profile_user@example.com", password="pass")

        # Update the profile with new bio and name
        response = client.post('/profile', json={
            "bio": "This is my new bio",
            "name": "Profile User Updated"
        })
        json_data = response.get_json()

        # Assert successful update
        assert response.status_code == 200, "Expected status code 200 for successful profile update."
        assert json_data["updated_profile"]["bio"] == "This is my new bio", "Bio was not updated correctly."
        assert json_data["updated_profile"]["name"] == "Profile User Updated", "Name was not updated correctly."

    def test_get_followings(self, client, create_user, login_user, db_session):
        """
        Test that a user can retrieve their followings correctly.
        """
        # Create main_user and followed_user with explicit names
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

        # Establish follow relationship
        follow = Follow(
            follower_id=main_user.user_id,
            followed_id=followed_user.user_id
        )
        db_session.add(follow)
        db_session.commit()

        # Log in as main_user
        login_user(email="main_user@example.com", password="pass")

        # Retrieve followings
        response = client.get('/profile')
        assert response.status_code == 200, "Expected status code 200 when retrieving followings."
        json_data = response.get_json()

        # Assert that 'followed_user' is in the followings list
        assert "followed_user" in json_data["followings"], (
            f"Expected 'followed_user' in followings, but got {json_data['followings']}"
        )

    def test_get_others_profile(self, client, create_user, login_user, db_session):
        """
        Test that a user can retrieve another user's profile correctly.
        """
        # Create other_user with a specific name
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

        # Log in as main_user
        login_user(email="main_user@example.com", password="pass")

        # Fetch other_user's profile
        response = client.get(f'/profile/{other_user.user_id}')
        assert response.status_code == 200, "Expected status code 200 when retrieving another user's profile."
        json_data = response.get_json()

        # Assert that the name matches
        assert json_data["name"] == "other_user", (
            f"Expected name 'other_user', but got '{json_data['name']}'"
        )

    def test_follow_unfollow(self, client, create_user, login_user, db_session):
        """
        Test that a user can follow and unfollow another user successfully.
        """
        # Create two distinct users
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

        # Log in as user_a
        login_user(email="user_a@example.com", password="pass")

        # Follow user_b
        res = client.post('/follow', json={"user_id": target.user_id})
        assert res.status_code == 200, (
            f"Expected status code 200 when following, but got {res.status_code}. Response: {res.get_json()}"
        )
        data = res.get_json()
        assert data["success"] == "Successfully followed user", (
            f"Expected success message, but got '{data.get('success')}'"
        )

        # Verify the follow relationship exists in the database
        follow = db_session.query(Follow).filter_by(
            follower_id=user.user_id,
            followed_id=target.user_id
        ).first()
        assert follow is not None, "Follow relationship was not created in the database."

        # Unfollow user_b
        res = client.post('/unfollow', json={"user_id": target.user_id})
        assert res.status_code == 200, (
            f"Expected status code 200 when unfollowing, but got {res.status_code}. Response: {res.get_json()}"
        )
        data = res.get_json()
        assert data["success"] == "Successfully unfollowed user", (
            f"Expected success message, but got '{data.get('success')}'"
        )

        # Confirm the follow relationship no longer exists
        follow = db_session.query(Follow).filter_by(
            follower_id=user.user_id,
            followed_id=target.user_id
        ).first()
        assert follow is None, "Follow relationship was not removed from the database."
