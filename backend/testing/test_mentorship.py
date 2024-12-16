"""import pytest
from datetime import datetime, timedelta
from backend.database.create import MentorshipSession
from backend.config import COST_TO_BOOK_MENTORSHIP, REWARD_FOR_MENTORING


@pytest.mark.usefixtures("client", "db_session")
class TestMentorship:
    def test_book_mentorship_unauthenticated(self, client):
        response = client.post('/mentorship/book', json={
            "mentor_id": 1,
            "scheduled_time": "2100-01-01T10:00:00"
        })
        assert response.status_code == 401

    def test_book_mentorship_insufficient_credits(self, client, create_user, login_user):
        # Create mentee with 0 credits and mentor with availability
        mentee = create_user(username="mentee", email="mentee@example.com", password="pass", credits=0)
        create_user(username="mentor", email="mentor@example.com", password="pass", mentorship_availability=True)

        # Log in as mentee
        login_user(email="mentee@example.com", password="pass")

        # Try to book mentorship
        future_time = (datetime.utcnow() + timedelta(days=1)).isoformat()
        response = client.post('/mentorship/book', json={
            "mentor_id": mentee.user_id,
            "scheduled_time": future_time
        })

        assert response.status_code == 403
        json_data = response.get_json()
        assert json_data["error"] == "Insufficient credits"

    def test_book_mentorship_success(self, client, create_user, login_user, db_session, monkeypatch):
        # Mock Google Calendar event creation
        def mock_create_event(*args, **kwargs):
            return "mock_event_id"
        from backend.google_calendar import create_google_calendar_event
        monkeypatch.setattr("backend.google_calendar.create_google_calendar_event", mock_create_event)

        # Create mentee and mentor
        mentee = create_user(username="mentee", email="mentee@example.com", password="pass", credits=1000)
        mentor = create_user(username="mentor", email="mentor@example.com", password="pass", mentorship_availability=True)

        # Log in as mentee
        login_user(email="mentee@example.com", password="pass")

        # Book mentorship
        future_time = (datetime.utcnow() + timedelta(days=1)).isoformat()
        response = client.post('/mentorship/book', json={
            "mentor_id": mentor.user_id,
            "scheduled_time": future_time
        })

        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data["message"] == "Mentorship session booked successfully"

        # Verify credits deduction
        db_session.refresh(mentee)
        assert mentee.credits == 1000 - COST_TO_BOOK_MENTORSHIP

    def test_complete_mentorship_unauthorized(self, client, create_user, login_user, db_session):
        # Create mentor, mentee, and session
        mentor = create_user(username="mentor", email="mentor@example.com", password="pass", credits=1000)
        mentee = create_user(username="mentee", email="mentee@example.com", password="pass", credits=1000)

        session = MentorshipSession(
            mentor_id=mentor.user_id,
            mentee_id=mentee.user_id,
            scheduled_time=datetime.utcnow() + timedelta(days=1),
            status='scheduled',
            event_id="mock_event"
        )
        db_session.add(session)
        db_session.commit()

        # Log in as mentee and try to complete session
        login_user(email="mentee@example.com", password="pass")
        response = client.post(f'/mentorship/complete/{session.session_id}')
        assert response.status_code == 403
        json_data = response.get_json()
        assert json_data["error"] == "Unauthorized action"

    def test_complete_mentorship_success(self, client, create_user, login_user, db_session):
        # Create mentor, mentee, and session
        mentor = create_user(username="mentor", email="mentor@example.com", password="pass", credits=1000)
        mentee = create_user(username="mentee", email="mentee@example.com", password="pass", credits=1000)

        session = MentorshipSession(
            mentor_id=mentor.user_id,
            mentee_id=mentee.user_id,
            scheduled_time=datetime.utcnow() + timedelta(days=1),
            status='scheduled',
            event_id="mock_event"
        )
        db_session.add(session)
        db_session.commit()

        # Log in as mentor and complete session
        login_user(email="mentor@example.com", password="pass")
        response = client.post(f'/mentorship/complete/{session.session_id}')
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["message"] == "Mentorship session completed"

        # Verify mentor credits increased
        db_session.refresh(mentor)
        assert mentor.credits == 1000 + REWARD_FOR_MENTORING

    def test_cancel_mentorship(self, client, create_user, login_user, db_session, monkeypatch):
        # Mock Google Calendar event deletion
        def mock_delete_event(*args, **kwargs):
            return True
        from backend.google_calendar import delete_google_calendar_event
        monkeypatch.setattr("backend.google_calendar.delete_google_calendar_event", mock_delete_event)

        # Create mentor, mentee, and session
        mentee = create_user(username="mentee", email="mentee@example.com", password="pass", credits=1000)
        mentor = create_user(username="mentor", email="mentor@example.com", password="pass", credits=1000)

        session = MentorshipSession(
            mentor_id=mentor.user_id,
            mentee_id=mentee.user_id,
            scheduled_time=datetime.utcnow() + timedelta(days=1),
            status='scheduled',
            event_id="mock_event"
        )
        db_session.add(session)
        db_session.commit()

        # Log in as mentee and cancel session
        login_user(email="mentee@example.com", password="pass")
        response = client.post(f'/mentorship/cancel/{session.session_id}')
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["message"] == "Mentorship session canceled"

        # Verify credits refunded
        db_session.refresh(mentee)
        assert mentee.credits == 1000 + COST_TO_BOOK_MENTORSHIP
"""