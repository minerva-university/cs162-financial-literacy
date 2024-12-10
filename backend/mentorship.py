from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func
from .database.create import User, MentorshipSession, engine
from sqlalchemy.orm import sessionmaker
from .config import (
    COST_TO_BOOK_MENTORSHIP,
    REWARD_FOR_MENTORING,
)

# Define the blueprint
mentorship_bp = Blueprint('mentorship', __name__)
Session = sessionmaker(bind=engine)

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
        return jsonify({'error': 'Insufficient credits'}), 403

    # Deduct credits from the user
    user.credits -= COST_TO_BOOK_MENTORSHIP

    # Create a new mentorship session
    new_session = MentorshipSession(
        mentee_id=user.user_id,
        mentor_id=data['mentor_id'],
        scheduled_time=data['scheduled_time'],
        status='scheduled'
    )

    session.add(new_session)
    try:
        session.commit()
        return jsonify({
            'message': 'Mentorship session booked successfully',
            'session_id': new_session.session_id,
            'credits': user.credits
        }), 201
    except Exception as e:
        session.rollback()
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
        return jsonify({'error': 'Mentorship session not found'}), 404

    if mentorship_session.mentor_id != current_user.user_id:
        return jsonify({'error': 'Unauthorized action'}), 403

    if mentorship_session.status != 'scheduled':
        return jsonify({'error': 'Session cannot be completed'}), 400

    # Update session status and add credits to mentor
    mentorship_session.status = 'completed'
    mentor = session.query(User).filter(User.user_id == current_user.user_id).first()
    mentor.credits += REWARD_FOR_MENTORING

    try:
        session.commit()
        return jsonify({
            'message': 'Mentorship session completed',
            'credits': mentor.credits
        }), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500

# Endpoint to get upcoming mentorship sessions for a user
@mentorship_bp.route('/mentorship/upcoming', methods=['GET'])
@login_required
def get_upcoming_sessions():
    session = Session()
    sessions = session.query(MentorshipSession).filter(
        (MentorshipSession.mentee_id == current_user.user_id) | 
        (MentorshipSession.mentor_id == current_user.user_id),
        MentorshipSession.status == 'scheduled'
    ).all()

    session_list = []
    for s in sessions:
        mentor = session.query(User).filter(User.user_id == s.mentor_id).first()
        mentee = session.query(User).filter(User.user_id == s.mentee_id).first()
        session_list.append({
            'session_id': s.session_id,
            'mentor': {'id': s.mentor_id, 'name': mentor.name if mentor else 'Unknown'},
            'mentee': {'id': s.mentee_id, 'name': mentee.name if mentee else 'Unknown'},
            'scheduled_time': s.scheduled_time,
            'status': s.status
        })

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
        return jsonify({'error': 'Mentorship session not found'}), 404

    user = session.query(User).filter(User.user_id == current_user.user_id).first()

    if mentorship_session.mentee_id != user.user_id and mentorship_session.mentor_id != user.user_id:
        return jsonify({'error': 'Unauthorized action'}), 403

    if mentorship_session.status != 'scheduled':
        return jsonify({'error': 'Cannot cancel this session'}), 400

    # Update session status
    mentorship_session.status = 'canceled'

    # Refund credits if mentee cancels
    if mentorship_session.mentee_id == user.user_id:
        user.credits += COST_TO_BOOK_MENTORSHIP

    try:
        session.commit()
        return jsonify({'message': 'Mentorship session canceled', 'credits': user.credits}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500

# Endpoint to fetch mentorship history
@mentorship_bp.route('/mentorship/history', methods=['GET'])
@login_required
def get_mentorship_history():
    session = Session()
    sessions = session.query(MentorshipSession).filter(
        (MentorshipSession.mentee_id == current_user.user_id) | 
        (MentorshipSession.mentor_id == current_user.user_id)
    ).order_by(MentorshipSession.scheduled_time.desc()).all()

    history = []
    for s in sessions:
        mentor = session.query(User).filter(User.user_id == s.mentor_id).first()
        mentee = session.query(User).filter(User.user_id == s.mentee_id).first()
        history.append({
            'session_id': s.session_id,
            'mentor': {'id': s.mentor_id, 'name': mentor.name if mentor else 'Unknown'},
            'mentee': {'id': s.mentee_id, 'name': mentee.name if mentee else 'Unknown'},
            'scheduled_time': s.scheduled_time,
            'status': s.status
        })

    return jsonify({'mentorship_history': history}), 200

@mentorship_bp.route('/mentorship/sessions', methods=['GET'])
@login_required
def get_scheduled_sessions():
    session = Session()
    sessions = session.query(MentorshipSession).filter(
        (MentorshipSession.mentee_id == current_user.user_id) |
        (MentorshipSession.mentor_id == current_user.user_id),
        MentorshipSession.status == 'scheduled'
    ).all()

    session_list = [
        {
            'session_id': s.session_id,
            'mentor': s.mentor_id,
            'mentee': s.mentee_id,
            'scheduled_time': s.scheduled_time,
            'status': s.status
        } for s in sessions
    ]

    return jsonify({'sessions': session_list}), 200

@mentorship_bp.route('/mentorship/feedback', methods=['POST'])
@login_required
def add_feedback():
    data = request.get_json()
    session_id = data.get('session_id')
    feedback = data.get('feedback')

    if not session_id or not feedback:
        return jsonify({'error': 'Session ID and feedback are required'}), 400

    session = Session()
    mentorship_session = session.query(MentorshipSession).filter_by(
        session_id=session_id
    ).first()

    if not mentorship_session or mentorship_session.mentee_id != current_user.user_id:
        return jsonify({'error': 'Invalid session or unauthorized action'}), 403

    mentorship_session.feedback = feedback

    try:
        session.commit()
        return jsonify({'message': 'Feedback added successfully'}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
