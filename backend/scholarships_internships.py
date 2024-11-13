from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from sqlalchemy.orm import sessionmaker
from .database.create import Organization, engine, Scholarship, Internship, User  # Adjust the import according to your file structure

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

@scholarships_internships.route('/scholarships/<int:scholarship_id>', methods=['GET'])
@login_required
def get_scholarship_by_id(scholarship_id):
    session = Session()
    try:
        # Fetch the scholarship with the given ID
        scholarship = session.query(Scholarship).filter_by(scholarship_id=scholarship_id).first()

        if not scholarship:
            return jsonify({"error": "Scholarship not found"}), 404

        # Return detailed scholarship data
        return jsonify({
            'id': scholarship.scholarship_id,
            'title': scholarship.title,
            'provider': scholarship.organization.name if scholarship.organization else None,
            'description': scholarship.description,
            'amount': scholarship.amount,
            'eligibility': scholarship.requirements,
            'application_link': scholarship.application_link,
            'deadline': scholarship.deadline,
            'created_at': scholarship.created_at,
            'updated_at': scholarship.updated_at
        })
    finally:
        session.close()


@scholarships_internships.route('/scholarships/filter', methods=['GET'])
@login_required
def filter_scholarships():
    # Start a session
    session = Session()
    try:
        # Get filter parameters from the request
        title = request.args.get('title')  # Filter by scholarship title
        organization = request.args.get('organization')  # Filter by organization name
        min_amount = request.args.get('min_amount', type=int)  # Filter by minimum amount
        
        # Start the base query for scholarships
        query = session.query(Scholarship)
        
        # Apply filters dynamically based on the query parameters
        if title:
            query = query.filter(Scholarship.title.ilike(f"%{title}%"))  # Case-insensitive filter for title
        if organization:
            query = query.join(Organization).filter(Organization.name.ilike(f"%{organization}%"))  # Case-insensitive filter for organization
        if min_amount is not None:
            query = query.filter(Scholarship.amount >= min_amount)  # Filter by minimum amount
        
        # Execute the query
        results = query.all()

        # Return the filtered results as JSON
        return jsonify([{
            'id': scholarship.scholarship_id,
            'title': scholarship.title,
            'description': scholarship.description,
            'organization': scholarship.organization.name if scholarship.organization else None,
            'amount': scholarship.amount,
            'deadline': scholarship.deadline
        } for scholarship in results])

    finally:
        # Close the session after use
        session.close()

@scholarships_internships.route('/scholarships/<int:scholarship_id>', methods=['PUT'])
@login_required
def update_scholarship(scholarship_id):
    data = request.json
    session = Session()
    try:
        # Query for the scholarship based on the provided ID and ensure it belongs to the current user
        scholarship = session.query(Scholarship).filter_by(scholarship_id=scholarship_id, user_id=current_user.id).first()
        
        if not scholarship:
            return jsonify({"error": "Scholarship not found or unauthorized"}), 404

        # Update the scholarship fields with the provided data or keep existing values
        scholarship.title = data.get('title', scholarship.title)
        scholarship.description = data.get('description', scholarship.description)
        scholarship.updated_at = datetime.now(timezone.utc)
        
        # Commit the changes to the database
        session.commit()
        
        return jsonify({"success": "Scholarship updated"})
    
    except Exception as e:
        session.rollback()
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

@scholarships_internships.route('/internships/<int:internship_id>', methods=['GET'])
@login_required
def get_internship_by_id(internship_id):
    session = Session()
    try:
        # Fetch the internship with the given ID
        internship = session.query(Internship).filter_by(internship_id=internship_id).first()

        if not internship:
            return jsonify({"error": "Internship not found"}), 404

        # Return detailed internship data
        return jsonify({
            'id': internship.internship_id,
            'title': internship.title,
            'company': internship.organization.name if internship.organization else None,
            'description': internship.description,
            'duration': internship.duration,
            'stipend': internship.stipend,
            'requirements': internship.requirements,
            'application_link': internship.application_link,
            'created_at': internship.created_at,
            'updated_at': internship.updated_at
        })
    finally:
        session.close()



@scholarships_internships.route('/internships/filter', methods=['GET'])
@login_required
def filter_internships():
    # Start a session
    session = Session()
    try:
        # Get filter parameters from the request
        title = request.args.get('title')  # Filter by title
        company = request.args.get('company')  # Filter by company name
        min_stipend = request.args.get('min_stipend', type=int)  # Filter by minimum stipend
        
        # Start the base query
        query = session.query(Internship)
        
        # Apply filters dynamically based on the query parameters
        if title:
            query = query.filter(Internship.title.ilike(f"%{title}%"))  # Case-insensitive filter for title
        if company:
            query = query.join(Organization).filter(Organization.name.ilike(f"%{company}%"))  # Case-insensitive filter for company
        if min_stipend is not None:
            query = query.filter(Internship.stipend >= min_stipend)  # Filter by minimum stipend
        
        # Execute the query
        results = query.all()

        # Return the filtered results as JSON
        return jsonify([{
            'id': internship.internship_id,
            'title': internship.title,
            'description': internship.description,
            'company': internship.organization.name if internship.organization else None,
            'duration': internship.duration,
            'stipend': internship.stipend
        } for internship in results])

    finally:
        # Close the session after use
        session.close()

@scholarships_internships.route('/user/internships', methods=['GET'])
@login_required
def user_internships():
    session = Session()
    try:
        user_internships = session.query(Internship).filter_by(user_id=current_user.id).all()
        return jsonify([{
            'id': internship.internship_id,
            'title': internship.title,
            'description': internship.description,
            'stipend': internship.stipend
        } for internship in user_internships])
    finally:
        session.close()

@scholarships_internships.route('/internships/<int:id>', methods=['PUT'])
@login_required
def update_internship(internship_id):
    data = request.json
    session = Session()
    try:
        internship = session.query(Internship).filter_by(internship_id=internship_id, user_id=current_user.internship_id).first()
        if not internship:
            return jsonify({"error": "Internship not found or unauthorized"}), 404

        internship.title = data.get('title', internship.title)
        internship.description = data.get('description', internship.description)
        internship.updated_at = datetime.now(timezone.utc)
        
        session.commit()
        return jsonify({"success": "Internship updated"})
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

