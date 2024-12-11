# tests/test_mentorship.py
import pytest
from datetime import datetime, timedelta
from backend.database.create import User, MentorshipSession
from backend.config import COST_TO_BOOK_MENTORSHIP, REWARD_FOR_MENTORING

@pytest.mark.usefixtures("client", "db_session")
class TestMentorship:
    def test_book_mentorship_unauthenticated(self, client):
        res = client.post('/mentorship/book', json={"mentor_id": 1, "scheduled_time": "2100-01-01T10:00:00"})
        assert res.status_code == 401

    def test_book_mentorship_insufficient_credits(self, client, db_session):
        mentee = User(username="mentee", email="mentee@example.com", credits=0)
        mentee.set_password("pass")
        mentor = User(username="mentor", email="mentor@example.com", credits=100, mentorship_availability=True)
        mentor.set_password("pass")
        db_session.add_all([mentee, mentor])
        db_session.commit()

        client.post('/login', json={
            "email": "mentee@example.com",
            "password": "pass"
        })

        future_time = (datetime.utcnow() + timedelta(days=1)).isoformat()
        res = client.post('/mentorship/book', json={"mentor_id": mentor.user_id, "scheduled_time": future_time})
        data = res.get_json()
        assert res.status_code == 403
        assert data["error"] == "Insufficient credits"

    def test_book_mentorship_success(self, client, db_session, monkeypatch):
        # Mock Google Calendar event creation
        def mock_create_event(*args, **kwargs):
            return "mock_event_id"
        from backend.google_calendar import create_google_calendar_event
        monkeypatch.setattr("backend.google_calendar.create_google_calendar_event", mock_create_event)

        mentee = User(username="mentee2", email="mentee2@example.com", credits=1000)
        mentee.set_password("pass")
        mentor = User(username="mentor2", email="mentor2@example.com", credits=100, mentorship_availability=True)
        mentor.set_password("pass")
        db_session.add_all([mentee, mentor])
        db_session.commit()

        client.post('/login', json={
            "email": "mentee2@example.com",
            "password": "pass"
        })

        future_time = (datetime.utcnow() + timedelta(days=1)).isoformat()
        res = client.post('/mentorship/book', json={"mentor_id": mentor.user_id, "scheduled_time": future_time})
        data = res.get_json()
        assert res.status_code == 201
        assert data["message"] == "Mentorship session booked successfully"

        # Credits should be deducted
        db_session.refresh(mentee)
        assert mentee.credits == 1000 - COST_TO_BOOK_MENTORSHIP

    def test_complete_mentorship_unauthorized(self, client, db_session):
        mentor = User(username="mentor3", email="mentor3@example.com", credits=1000)
        mentor.set_password("pass")
        mentee = User(username="mentee3", email="mentee3@example.com", credits=1000)
        mentee.set_password("pass")
        db_session.add_all([mentor, mentee])
        db_session.commit()

        session = MentorshipSession(
            mentor_id=mentor.user_id,
            mentee_id=mentee.user_id,
            scheduled_time=datetime.utcnow() + timedelta(days=1),
            status='scheduled',
            event_id="mock_event"
        )
        db_session.add(session)
        db_session.commit()

        # Login as mentee, try to complete session
        client.post('/login', json={
            "email": "mentee3@example.com",
            "password": "pass"
        })

        res = client.post(f'/mentorship/complete/{session.session_id}')
        assert res.status_code == 403
        data = res.get_json()
        assert data["error"] == "Unauthorized action"

    def test_complete_mentorship_success(self, client, db_session):
        mentor = User(username="mentor4", email="mentor4@example.com", credits=1000)
        mentor.set_password("pass")
        mentee = User(username="mentee4", email="mentee4@example.com", credits=1000)
        mentee.set_password("pass")
        db_session.add_all([mentor, mentee])
        db_session.commit()

        session = MentorshipSession(
            mentor_id=mentor.user_id,
            mentee_id=mentee.user_id,
            scheduled_time=datetime.utcnow() + timedelta(days=1),
            status='scheduled',
            event_id="mock_event"
        )
        db_session.add(session)
        db_session.commit()

        client.post('/login', json={
            "email": "mentor4@example.com",
            "password": "pass"
        })

        res = client.post(f'/mentorship/complete/{session.session_id}')
        assert res.status_code == 200
        data = res.get_json()
        assert data["message"] == "Mentorship session completed"

        # Mentor should get REWARD_FOR_MENTORING
        db_session.refresh(mentor)
        assert mentor.credits == 1000 + REWARD_FOR_MENTORING

    def test_cancel_mentorship(self, client, db_session, monkeypatch):
        # Mock delete_google_calendar_event to not fail
        def mock_delete_event(*args, **kwargs):
            return True
        from backend.google_calendar import delete_google_calendar_event
        monkeypatch.setattr("backend.google_calendar.delete_google_calendar_event", mock_delete_event)

        mentee = User(username="mentee5", email="mentee5@example.com", credits=1000)
        mentee.set_password("pass")
        mentor = User(username="mentor5", email="mentor5@example.com", credits=1000)
        mentor.set_password("pass")
        db_session.add_all([mentee, mentor])
        db_session.commit()

        session_ = MentorshipSession(
            mentor_id=mentor.user_id,
            mentee_id=mentee.user_id,
            scheduled_time=datetime.utcnow() + timedelta(days=1),
            status='scheduled',
            event_id="mock_event"
        )
        db_session.add(session_)
        db_session.commit()

        client.post('/login', json={
            "email": "mentee5@example.com",
            "password": "pass"
        })

        # Cancel session as mentee
        res = client.post(f'/mentorship/cancel/{session_.session_id}')
        assert res.status_code == 200
        data = res.get_json()
        assert data["message"] == "Mentorship session canceled"

        # Check credits refunded
        db_session.refresh(mentee)
        assert mentee.credits == 1000 + COST_TO_BOOK_MENTORSHIP
