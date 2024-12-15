# mentorship.py

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
        return scheduled_time
    except Exception:
        raise ValueError("Invalid time format. Use ISO format (YYYY-MM-DDTHH:MM:SS)")

# Endpoint to get available mentors
@mentorship_bp.route('/mentors/available', methods=['GET'])
@login_required
def get_available_mentors():

    print("Getting available mentors")
    session = Session()
    try:
        # Assuming you have a field in the User model to indicate availability
        available_mentors = session.query(User).filter(User.mentorship_availability == True).all()
        
        mentors_list = [{
            'id': mentor.user_id,
            'name': mentor.username,
            'bio': mentor.bio,
            #'calendar_url': mentor.calendar_url
        } for mentor in available_mentors]
        print(f"Available mentors: {mentors_list}")
        return jsonify({'mentors': mentors_list}), 200
    except Exception as e:
        print(f"Error fetching available mentors: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        session.close()

# Endpoint to book a mentorship session
@mentorship_bp.route('/mentorship/book/<int:mentor_id>', methods=['POST'])
@login_required
def book_mentorship(mentor_id):
    mentee = current_user
    if mentee.credits < COST_TO_BOOK_MENTORSHIP:
        return jsonify({"error": "Insufficient credits"}), 403

    session = Session()
    user = session.query(User).filter(User.user_id == current_user.user_id).first()

    # Check if user has enough credits
    if user.credits < COST_TO_BOOK_MENTORSHIP:
        session.close()
        return jsonify({'error': 'Insufficient credits'}), 403

    # Parse and validate scheduled time
    try:
        scheduled_time = parse_scheduled_time(data['scheduled_time'])
        print("Parsed Time")
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
        #event_id = create_google_calendar_event(
        #    mentor_email=mentor.email,
        #    mentee_email=user.email,
        #    mentor_name=mentor.username,
        #    mentee_name=user.username,
        #    start_time=scheduled_time.isoformat(),
        #    end_time=end_time.isoformat()
        #)
        ...
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
        status='pending',
        #event_id=event_id
    )

    session.add(new_session)
    try:
        
        credits = user.credits
        session.commit()
        session_id = new_session.session_id
        session.close()

        return jsonify({
            'message': 'Mentorship session booked successfully',
            'session_id': session_id,
            'credits': credits
        }), 201
    except Exception as e:
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
@mentorship_bp.route('/mentorship/mentor_requests', methods=['GET'])
@login_required
def get_upcoming_sessions():
    session = Session()
    sessions = session.query(MentorshipSession).filter(
        MentorshipSession.mentor_id == current_user.user_id
    ).all()

    session_list = []
    for s in sessions:
        mentor = s.mentor
        mentee = s.mentee
        session_list.append({
            'session_id': s.session_id,
            'mentor': {'id': s.mentor_id, 'name': mentor.name if mentor else 'Unknown'},
            'mentee': {'id': s.mentee_id, 'name': mentee.name if mentee else 'Unknown'},
            'scheduled_time': s.scheduled_time.isoformat(),
            'status': s.status
        })

    session.close()
    return jsonify({'upcoming_sessions': session_list}), 200

# Endpoint to update a mentorship session
@mentorship_bp.route('/mentorship/update/<int:session_id>', methods=['POST'])
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

    if mentorship_session.mentor_id != user.user_id:
        session.close()
        return jsonify({'error': 'Unauthorized action'}), 403

    if mentorship_session.status != 'pending':
        session.close()
        return jsonify({'error': 'Cannot update this session'}), 400

    if "type" not in request.json:
        return jsonify({'error': 'Include the type of the update'}), 400
    
    if request.json["type"] == "canceled":
        mentorship_session.status = 'canceled'
    elif request.json["type"] == "scheduled":
        mentorship_session.status = 'scheduled'
    else:
        return jsonify({'error': 'Include a valid type of the update ("canceled", "scheduled")'}), 400


    # Refund credits if mentor cancels
    if request.json["type"] == "cancelled":
        mentorship_session.mentee.credits += COST_TO_BOOK_MENTORSHIP

    # Rewarding credits if mentor approved
    if request.json["type"] == "approved":
        mentorship_session.mentor.credits += REWARD_FOR_MENTORING

    try:
        session.commit()
        session.close()
        return jsonify({'message': f'Mentorship session {request.json["type"]}'}), 200
    except Exception as e:
        session.rollback()
        session.close()
        return jsonify({'error': str(e)}), 500

@mentorship_bp.route('/mentors/availability', methods=['POST'])
@login_required
def update_mentorship_availability():
    session = Session()
    try:
        data = request.get_json()
        if 'availability' not in data:
            return jsonify({'error': 'Availability status is required'}), 400

        # Update the current user's availability
        user = session.query(User).filter(User.user_id == current_user.user_id).first()
        user.mentorship_availability = data['availability'] == 'yes'
        session.commit()

        return jsonify({'message': 'Availability updated successfully'}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()