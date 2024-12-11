from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from .database.create import User, MentorshipSession, engine
from .config import (
    COST_TO_BOOK_MENTORSHIP,
    REWARD_FOR_MENTORING,
)
from .google_calendar import create_google_calendar_event, delete_google_calendar_event

mentorship_bp = Blueprint('mentorship', __name__)
Session = sessionmaker(bind=engine)

# Helper function to parse and validate scheduled times
def parse_scheduled_time(time_str):
    """
    Parses and validates the scheduled time string in ISO format.

    Args:
        time_str (str): Scheduled time in ISO format.

    Returns:
        datetime: Parsed datetime object.

    Raises:
        ValueError: If the time is in the past or invalid.
    """
    try:
        scheduled_time = datetime.fromisoformat(time_str)
        if scheduled_time <= datetime.utcnow():
            raise ValueError("Scheduled time must be in the future")
        return scheduled_time
    except Exception:
        raise ValueError("Invalid time format. Use ISO format (YYYY-MM-DDTHH:MM:SS)")

# Endpoint to book a mentorship session
@mentorship_bp.route('/mentorship/book', methods=['POST'])
@login_required
def book_mentorship():
    data = request.get_json()
    if not data or 'mentor_id' not in data or 'scheduled_time' not in data:
        return jsonify({'error': 'Mentor ID and scheduled time are required'}), 400

    session = Session()
    user = session.query(User).filter(User.user_id == current_user.user_id).first()

    # Check if user has enough credits
    if user.credits < COST_TO_BOOK_MENTORSHIP:
        session.close()
        return jsonify({'error': 'Insufficient credits'}), 403

    # Parse and validate scheduled time
    try:
        scheduled_time = parse_scheduled_time(data['scheduled_time'])
    except ValueError as e:
        session.close()
        return jsonify({'error': str(e)}), 400

    # Check mentor existence
    mentor = session.query(User).filter(User.user_id == data['mentor_id']).first()
    if not mentor:
        session.close()
        return jsonify({'error': 'Mentor not found'}), 404

    # Deduct credits from the user
    user.credits -= COST_TO_BOOK_MENTORSHIP

    # Assume each session lasts 1 hour
    end_time = scheduled_time + timedelta(hours=1)

    # Create the event in Google Calendar
    try:
        event_id = create_google_calendar_event(
            mentor_email=mentor.email,
            mentee_email=user.email,
            mentor_name=mentor.username,
            mentee_name=user.username,
            start_time=scheduled_time.isoformat(),
            end_time=end_time.isoformat()
        )
    except Exception as gc_err:
        # Rollback credit deduction if event creation fails
        user.credits += COST_TO_BOOK_MENTORSHIP
        session.commit()
        session.close()
        return jsonify({'error': f"Failed to create calendar event: {str(gc_err)}"}), 500

    # Create a new mentorship session
    new_session = MentorshipSession(
        mentee_id=user.user_id,
        mentor_id=data['mentor_id'],
        scheduled_time=scheduled_time,
        status='scheduled',
        event_id=event_id
    )

    session.add(new_session)
    try:
        session.commit()
        session.close()
        return jsonify({
            'message': 'Mentorship session booked successfully',
            'session_id': new_session.session_id,
            'credits': user.credits
        }), 201
    except Exception as e:
        # Remove the created Google Calendar event if DB commit fails
        delete_google_calendar_event(event_id)
        session.rollback()
        session.close()
        return jsonify({'error': str(e)}), 500

# Endpoint for mentor to complete a mentorship session
@mentorship_bp.route('/mentorship/complete/<int:session_id>', methods=['POST'])
@login_required
def complete_mentorship(session_id):
    session = Session()
    mentorship_session = session.query(MentorshipSession).filter(
        MentorshipSession.session_id == session_id
    ).first()

    if not mentorship_session:
        session.close()
        return jsonify({'error': 'Mentorship session not found'}), 404

    if mentorship_session.mentor_id != current_user.user_id:
        session.close()
        return jsonify({'error': 'Unauthorized action'}), 403

    if mentorship_session.status != 'scheduled':
        session.close()
        return jsonify({'error': 'Session cannot be completed'}), 400

    # Update session status and add credits to mentor
    mentorship_session.status = 'completed'
    mentor = session.query(User).filter(User.user_id == current_user.user_id).first()
    mentor.credits += REWARD_FOR_MENTORING

    try:
        session.commit()
        session.close()
        return jsonify({
            'message': 'Mentorship session completed',
            'credits': mentor.credits
        }), 200
    except Exception as e:
        session.rollback()
        session.close()
        return jsonify({'error': str(e)}), 500

# Endpoint to get upcoming mentorship sessions for a user
@mentorship_bp.route('/mentorship/upcoming', methods=['GET'])
@login_required
def get_upcoming_sessions():
    session = Session()
    sessions = session.query(MentorshipSession).filter(
        ((MentorshipSession.mentee_id == current_user.user_id) | 
         (MentorshipSession.mentor_id == current_user.user_id)) &
        (MentorshipSession.status == 'scheduled')
    ).all()

    session_list = []
    for s in sessions:
        mentor = session.query(User).filter(User.user_id == s.mentor_id).first()
        mentee = session.query(User).filter(User.user_id == s.mentee_id).first()
        session_list.append({
            'session_id': s.session_id,
            'mentor': {'id': s.mentor_id, 'name': mentor.username if mentor else 'Unknown'},
            'mentee': {'id': s.mentee_id, 'name': mentee.username if mentee else 'Unknown'},
            'scheduled_time': s.scheduled_time.isoformat(),
            'status': s.status
        })

    session.close()
    return jsonify({'upcoming_sessions': session_list}), 200

# Endpoint to cancel a mentorship session
@mentorship_bp.route('/mentorship/cancel/<int:session_id>', methods=['POST'])
@login_required
def cancel_mentorship(session_id):
    session = Session()
    mentorship_session = session.query(MentorshipSession).filter(
        MentorshipSession.session_id == session_id
    ).first()

    if not mentorship_session:
        session.close()
        return jsonify({'error': 'Mentorship session not found'}), 404

    user = session.query(User).filter(User.user_id == current_user.user_id).first()

    if mentorship_session.mentee_id != user.user_id and mentorship_session.mentor_id != user.user_id:
        session.close()
        return jsonify({'error': 'Unauthorized action'}), 403

    if mentorship_session.status != 'scheduled':
        session.close()
        return jsonify({'error': 'Cannot cancel this session'}), 400

    # Update session status
    mentorship_session.status = 'canceled'

    # Refund credits if mentee cancels
    if mentorship_session.mentee_id == user.user_id:
        user.credits += COST_TO_BOOK_MENTORSHIP

    # Delete event from Google Calendar if exists
    if mentorship_session.event_id:
        try:
            delete_google_calendar_event(mentorship_session.event_id)
        except Exception as gc_err:
            pass

    try:
        session.commit()
        session.close()
        return jsonify({'message': 'Mentorship session canceled', 'credits': user.credits}), 200
    except Exception as e:
        session.rollback()
        session.close()
        return jsonify({'error': str(e)}), 500
