# tests/test_profile.py
import pytest
from backend.database.create import User, Follow

@pytest.mark.usefixtures("client", "db_session")
class TestProfile:
    def test_get_own_profile_unauthenticated(self, client):
        response = client.get('/profile')
        # Should be redirected or 401 because login_required
        assert response.status_code == 401

    def test_update_profile(self, client, db_session):
        user = User(username="profile_user", email="profile_user@example.com")
        user.set_password("pass")
        db_session.add(user)
        db_session.commit()

        # Login
        client.post('/login', json={
            "email": "profile_user@example.com",
            "password": "pass"
        })

        response = client.post('/profile', json={
            "bio": "This is my new bio",
            "name": "Profile User Updated"
        })
        json_data = response.get_json()
        assert response.status_code == 200
        assert json_data["updated_profile"]["bio"] == "This is my new bio"
        assert json_data["updated_profile"]["name"] == "Profile User Updated"

    def test_get_followings(self, client, db_session):
        user = User(user_id=1, username="main_user", email="main_user@example.com")
        followed_user = User(user_id=2, username="followed_user", email="followed_user@example.com")
        db_session.add_all([user, followed_user])
        db_session.commit()

        user.following.append(followed_user)
        db_session.commit()

        client.post('/login', json={
            "email": "main_user@example.com",
            "password": "pass"
        })

        response = client.get('/profile/followings')
        json_data = response.get_json()
        assert 'followed_user' in json_data

    def test_get_others_profile(self, client, db_session):
        user = User(username="other_user", email="other_user@example.com")
        user.set_password("pass")
        db_session.add(user)
        db_session.commit()

        # Login a different user
        main_user = User(username="main_user2", email="main_user2@example.com")
        main_user.set_password("pass")
        db_session.add(main_user)
        db_session.commit()

        client.post('/login', json={
            "email": "main_user2@example.com",
            "password": "pass"
        })

        response = client.get(f'/profile/{user.user_id}')
        json_data = response.get_json()
        assert json_data["name"] == "other_user"

    def test_follow_unfollow(self, client, db_session):
        user = User(username="user_a", email="user_a@example.com")
        user.set_password("pass")
        target = User(username="user_b", email="user_b@example.com")
        target.set_password("pass")
        db_session.add_all([user, target])
        db_session.commit()

        # Login user_a
        client.post('/login', json={
            "email": "user_a@example.com",
            "password": "pass"
        })

        # Follow user_b
        res = client.post('/follow', json={"user_id": target.user_id})
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] == "Successfully followed user"

        # Unfollow user_b
        res = client.post('/unfollow', json={"user_id": target.user_id})
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] == "Successfully unfollowed user"
