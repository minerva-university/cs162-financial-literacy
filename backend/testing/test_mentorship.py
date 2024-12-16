import pytest
from datetime import datetime, timedelta
from backend.database.create import User, MentorshipSession

@pytest.mark.usefixtures("client", "db_session")
class TestMentorship:

    def test_get_available_mentors(self, client, create_user, login_user, db_session):
        # Clear the database to ensure no residual users
        db_session.query(User).delete()
        db_session.commit()
        
        # Create test users with defined names
        mentor = create_user(username="mentor_user", email="mentor@example.com", password="pass", name="Mentor Name", mentorship_availability=True)
        mentee = create_user(username="mentee_user", email="mentee@example.com", password="pass", name="Mentee Name", mentorship_availability=False)
        login_response = login_user(email="mentee@example.com", password="pass")
        assert login_response.status_code == 200
        
        # Test the endpoint
        response = client.get('/mentors/available')
        assert response.status_code == 200
        json_data = response.get_json()
        assert "mentors" in json_data
        assert len(json_data["mentors"]) > 0

    def test_book_mentorship_insufficient_credits(self, client, create_user, login_user):
        mentee = create_user(username="low_credit_mentee", email="low@example.com", password="pass", name="Low Credit Mentee", credits=0)
        mentor = create_user(username="mentor_user", email="mentor@example.com", password="pass", name="Mentor Name")
        login_response = login_user(email="low@example.com", password="pass")
        assert login_response.status_code == 200

        response = client.post('/mentorship/book', json={
            "mentor_id": mentor.user_id,
            "scheduled_time": (datetime.now() + timedelta(days=1)).isoformat()
        })
        assert response.status_code == 403
        json_data = response.get_json()
        assert json_data["error"] == "Insufficient credits"

    def test_book_mentorship_success(self, client, create_user, login_user, db_session):
        mentee = create_user(username="rich_mentee_1", email="rich1@example.com", password="pass", name="Rich Mentee", credits=100)
        mentor = create_user(username="mentor_user_1", email="mentor1@example.com", password="pass", name="Mentor Name")
        db_session.commit()
        
        login_response = login_user(email="rich1@example.com", password="pass")
        assert login_response.status_code == 200

        response = client.post('/mentorship/book', json={
            "mentor_id": mentor.user_id,
            "scheduled_time": (datetime.now() + timedelta(days=1)).isoformat()
        })
        assert response.status_code == 201
        json_data = response.get_json()
        assert "session_id" in json_data
        assert json_data["credits"] < mentee.credits

    def test_update_availability_success(self, client, create_user, login_user, db_session):
        user = create_user(username="mentor_user", email="mentor@example.com", password="pass", name="Mentor Name")
        db_session.commit()

        login_response = login_user(email="mentor@example.com", password="pass")
        assert login_response.status_code == 200

        response = client.post('/mentors/availability', json={"availability": "yes"})
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["message"] == "Availability updated successfully"

    def test_get_upcoming_sessions(self, client, create_user, login_user, db_session):
        mentor = create_user(username="mentor_user", email="mentor@example.com", password="pass", name="Mentor Name")
        mentee = create_user(username="mentee_user", email="mentee@example.com", password="pass", name="Mentee Name")
        
        session = MentorshipSession(
            mentee_id=mentee.user_id,
            mentor_id=mentor.user_id,
            scheduled_time=datetime.now() + timedelta(days=1),
            status="pending"
        )
        db_session.add(session)
        db_session.commit()

        login_response = login_user(email="mentor@example.com", password="pass")
        assert login_response.status_code == 200

        response = client.get('/mentorship/mentor_requests')
        assert response.status_code == 200
        json_data = response.get_json()
        assert "upcoming_sessions" in json_data
        # Check that we have at least one session and that the last one has "pending" status
        assert len(json_data["upcoming_sessions"]) > 0
        assert json_data["upcoming_sessions"][-1]["status"] == "pending"
