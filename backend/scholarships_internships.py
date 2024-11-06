from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from flask_login import login_required
from sqlalchemy.orm import sessionmaker
from .database.create import engine, Scholarship, Internship, User  # Adjust the import according to your file structure

# Create a new session factory
Session = sessionmaker(bind=engine)
scholarships_internships = Blueprint('scholarships_internships', __name__)

@scholarships_internships.route('/scholarships', methods=['GET'])
@login_required
def get_scholarships():
    session = Session()
    try:
        # Fetch all scholarships from the database
        scholarships = session.query(Scholarship).all()
        return jsonify([{
            'id': scholarship.scholarship_id,
            'title': scholarship.title,
            'provider': scholarship.organization.name if scholarship.organization else None,
            'description': scholarship.description,
            'amount': scholarship.amount,
            'eligibility': scholarship.requirements,
            'application_link': scholarship.application_link,
            'deadline': scholarship.deadline
        } for scholarship in scholarships])
    finally:
        session.close()

@scholarships_internships.route('/scholarships', methods=['POST'])
@login_required
def post_scholarship():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    session = Session()
    try:
        scholarship = Scholarship(
            user_id=data.get('user_id'),  # Assuming you get user_id from request
            title=data.get('title'),
            description=data.get('description'),
            requirements=data.get('eligibility'),
            application_link=data.get('application_link'),
            created_at=datetime.now(timezone.utc),  # Automatically set created time
            updated_at=datetime.now(timezone.utc)   # Automatically set updated time
        )
        
        session.add(scholarship)
        session.commit()
        return jsonify({"success": "Scholarship posted", "scholarship_id": scholarship.scholarship_id}), 201
    except Exception as e:
        session.rollback()  # Rollback on error
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@scholarships_internships.route('/internships', methods=['GET'])
@login_required
def get_internships():
    session = Session()
    try:
        # Fetch all internships from the database
        internships = session.query(Internship).all()
        return jsonify([{
            'id': internship.internship_id,
            'title': internship.title,
            'description': internship.description,
            'company': internship.organization.name if internship.organization else None,
            'duration': internship.duration,
            'stipend': internship.stipend
        } for internship in internships])
    finally:
        session.close()

@scholarships_internships.route('/internships', methods=['POST'])
@login_required
def post_internship():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    session = Session()
    try:
        internship = Internship(
            user_id=data.get('user_id'),  # Assuming you get user_id from request
            organization_id=data.get('organization_id'),  # Assuming you have an org ID
            title=data.get('title'),
            description=data.get('description'),
            requirements=data.get('requirements'),
            application_link=data.get('application_link'),
            created_at=datetime.now(timezone.utc),  # Automatically set created time
            updated_at=datetime.now(timezone.utc)   # Automatically set updated time
        )
        
        session.add(internship)
        session.commit()
        return jsonify({"success": "Internship posted", "internship_id": internship.internship_id}), 201
    except Exception as e:
        session.rollback()  # Rollback on error
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
