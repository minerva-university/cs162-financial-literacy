# scholarships_internships.py

from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from .database.create import Organization, engine, Scholarship, Internship, User, ListingStatus
from .config import COST_TO_ACCESS, REWARD_FOR_POSTING
from typing import Optional


# Create a new session factory
Session = sessionmaker(bind=engine)
scholarships_internships = Blueprint('scholarships_internships', __name__)

@scholarships_internships.route('/scholarships', methods=['GET'])
@login_required
def get_scholarships():
    session = Session()
    try:
        user = session.query(User).filter_by(user_id=current_user.user_id).first()

        # Check if user has enough credits
        if user.credits < COST_TO_ACCESS:
            return jsonify({'error': 'Insufficient credits'}), 403

        # Deduct credits
        user.credits -= COST_TO_ACCESS
        session.commit()

        # Fetch all scholarships from the database
        scholarships = session.query(Scholarship).all()
        return jsonify({
            'credits': user.credits,
            'scholarships': [{
                'id': scholarship.scholarship_id,
                'title': scholarship.title,
                'organization': scholarship.organization.name if scholarship.organization else None,
                'description': scholarship.description,
                'amount': scholarship.amount,
                'requirements': scholarship.requirements,
                'application_link': scholarship.application_link,
                'deadline': scholarship.deadline,
            } for scholarship in scholarships]
        })
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
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
            user_id=current_user.user_id,
            title=data.get('title'),
            description=data.get('description'),
            amount=data.get('amount'),
            requirements=data.get('requirements'),
            application_link=data.get('application_link'),
            deadline=datetime.strptime(data.get('deadline'),'%Y-%m-%d'),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        session.add(scholarship)

        # Reward the user for posting
        user = session.query(User).filter_by(user_id=current_user.user_id).first()
        user.credits += REWARD_FOR_POSTING

        session.commit()
        return jsonify({
            "success": "Scholarship posted",
            "scholarship_id": scholarship.scholarship_id,
            "credits": user.credits
        }), 201
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@scholarships_internships.route('/scholarships/<int:scholarship_id>', methods=['GET'])
@login_required
def get_scholarship_by_id(scholarship_id):
    session = Session()
    try:
        user = session.query(User).filter_by(user_id=current_user.user_id).first()

        # Check if user has enough credits
        if user.credits < COST_TO_ACCESS:
            return jsonify({'error': 'Insufficient credits'}), 403

        # Deduct credits
        user.credits -= COST_TO_ACCESS
        session.commit()

        # Fetch the scholarship with the given ID
        scholarship = session.query(Scholarship).filter_by(scholarship_id=scholarship_id).first()

        if not scholarship:
            return jsonify({"error": "Scholarship not found"}), 404

        # Return detailed scholarship data
        return jsonify({
            'credits': user.credits,
            'scholarship': {
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
            }
        })
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@scholarships_internships.route('/scholarships/filter', methods=['GET'])
@login_required
def filter_scholarships():
    session = Session()
    try:
        user = session.query(User).filter_by(user_id=current_user.user_id).first()

        # Check if user has enough credits
        if user.credits < COST_TO_ACCESS:
            return jsonify({'error': 'Insufficient credits'}), 403

        # Deduct credits
        user.credits -= COST_TO_ACCESS
        session.commit()

        # Get filter parameters from the request
        title = request.args.get('title')
        organization = request.args.get('organization')
        min_amount = request.args.get('min_amount', type=int)

        # Start the base query for scholarships
        query = session.query(Scholarship)

        # Apply filters dynamically based on the query parameters
        if title:
            query = query.filter(Scholarship.title.ilike(f"%{title}%"))
        if organization:
            query = query.join(Organization).filter(Organization.name.ilike(f"%{organization}%"))
        if min_amount is not None:
            query = query.filter(Scholarship.amount >= min_amount)

        # Execute the query
        results = query.all()

        # Return the filtered results as JSON
        return jsonify({
            'credits': user.credits,
            'scholarships': [{
                'id': scholarship.scholarship_id,
                'title': scholarship.title,
                'description': scholarship.description,
                'organization': scholarship.organization.name if scholarship.organization else None,
                'amount': scholarship.amount,
                'deadline': scholarship.deadline
            } for scholarship in results]
        })
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@scholarships_internships.route('/scholarships/<int:scholarship_id>', methods=['PUT'])
@login_required
def update_scholarship(scholarship_id):
    data = request.json
    session = Session()
    try:
        # Query for the scholarship based on the provided ID and ensure it belongs to the current user
        scholarship = session.query(Scholarship).filter_by(
            scholarship_id=scholarship_id,
            user_id=current_user.user_id
        ).first()

        if not scholarship:
            return jsonify({"error": "Scholarship not found or unauthorized"}), 404

        # Update the scholarship fields with the provided data or keep existing values
        scholarship.title = data.get('title', scholarship.title)
        scholarship.description = data.get('description', scholarship.description)
        scholarship.updated_at = datetime.now(timezone.utc)

        session.commit()
        return jsonify({"success": "Scholarship updated"})
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@scholarships_internships.route('/internships', methods=['GET'])
@login_required
def get_internships():
    session = Session()
    try:
        user = session.query(User).filter_by(user_id=current_user.user_id).first()

        # Check if user has enough credits
        if user.credits < COST_TO_ACCESS:
            return jsonify({'error': 'Insufficient credits'}), 403

        # Deduct credits
        user.credits -= COST_TO_ACCESS
        session.commit()

        # Fetch all internships from the database
        internships = session.query(Internship).all()
        return jsonify({
            'credits': user.credits,
            'internships': [{
                'id': internship.internship_id,
                'title': internship.title,
                'description': internship.description,
                'deadline': internship.deadline,
                'requirements': internship.requirements,
                'company': internship.organization.name if internship.organization else None,
            } for internship in internships]
        })
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
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
            user_id=current_user.user_id,
            organization_id=data.get('organization_id'),
            title=data.get('title'),
            description=data.get('description'),
            requirements=data.get('requirements'),
            application_link=data.get('application_link'),
            deadline=datetime.strptime(data.get('deadline'),'%Y-%m-%d'),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        session.add(internship)

        # Reward the user for posting
        user = session.query(User).filter_by(user_id=current_user.user_id).first()
        user.credits += REWARD_FOR_POSTING

        session.commit()
        return jsonify({
            "success": "Internship posted",
            "internship_id": internship.internship_id,
            "credits": user.credits
        }), 201
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@scholarships_internships.route('/internships/<int:internship_id>', methods=['GET'])
@login_required
def get_internship_by_id(internship_id):
    session = Session()
    try:
        user = session.query(User).filter_by(user_id=current_user.user_id).first()

        # Check if user has enough credits
        if user.credits < COST_TO_ACCESS:
            return jsonify({'error': 'Insufficient credits'}), 403

        # Deduct credits
        user.credits -= COST_TO_ACCESS
        session.commit()

        # Fetch the internship with the given ID
        internship = session.query(Internship).filter_by(internship_id=internship_id).first()

        if not internship:
            return jsonify({"error": "Internship not found"}), 404

        # Return detailed internship data
        return jsonify({
            'credits': user.credits,
            'internship': {
                'id': internship.internship_id,
                'title': internship.title,
                'company': internship.organization.name if internship.organization else None,
                'description': internship.description,
                'requirements': internship.requirements,
                'application_link': internship.application_link,
                'created_at': internship.created_at,
                'updated_at': internship.updated_at
            }
        })
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@scholarships_internships.route('/internships/filter', methods=['GET'])
@login_required
def filter_internships():
    session = Session()
    try:
        user = session.query(User).filter_by(user_id=current_user.user_id).first()

        # Check if user has enough credits
        if user.credits < COST_TO_ACCESS:
            return jsonify({'error': 'Insufficient credits'}), 403

        # Deduct credits
        user.credits -= COST_TO_ACCESS
        session.commit()

        # Get filter parameters from the request
        title = request.args.get('title')
        company = request.args.get('company')

        # Start the base query
        query = session.query(Internship)

        # Apply filters dynamically based on the query parameters
        if title:
            query = query.filter(Internship.title.ilike(f"%{title}%"))
        if company:
            query = query.join(Organization).filter(Organization.name.ilike(f"%{company}%"))

        # Execute the query
        results = query.all()

        # Return the filtered results as JSON
        return jsonify({
            'credits': user.credits,
            'internships': [{
                'id': internship.internship_id,
                'title': internship.title,
                'description': internship.description,
                'company': internship.organization.name if internship.organization else None,
            } for internship in results]
        })
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@scholarships_internships.route('/user/internships', methods=['GET'])
@login_required
def user_internships():
    session = Session()
    try:
        # Fetch internships posted by the current user
        internships = session.query(Internship).filter_by(user_id=current_user.user_id).all()
        return jsonify([{
            'id': internship.internship_id,
            'title': internship.title,
            'description': internship.description,
        } for internship in internships])
    finally:
        session.close()

@scholarships_internships.route('/internships/<int:internship_id>', methods=['PUT'])
@login_required
def update_internship(internship_id):
    data = request.json
    session = Session()
    try:
        internship = session.query(Internship).filter_by(
            internship_id=internship_id,
            user_id=current_user.user_id
        ).first()
        if not internship:
            return jsonify({"error": "Internship not found or unauthorized"}), 404

        internship.title = data.get('title', internship.title)
        internship.description = data.get('description', internship.description)
        internship.updated_at = datetime.now(timezone.utc)

        session.commit()
        return jsonify({"success": "Internship updated"})
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


# Updating scholarship/internship status 
def update_listing_status(session, model_class):
    """
    Update status of expired listings
    """
    current_time = datetime.now(timezone.utc)
    expired_listings = session.query(model_class).filter(
        model_class.status == ListingStatus.ACTIVE,
        model_class.deadline < current_time
    ).all()
    
    for listing in expired_listings:
        listing.status = ListingStatus.EXPIRED
    
    if expired_listings:
        session.commit()

@scholarships_internships.route('/scholarships/search', methods=['GET'])
@login_required
def scholarship_ordering_date():
    session = Session()
    try:
        user = session.query(User).filter_by(user_id=current_user.user_id).first()

        # Check if user has enough credits
        if user.credits < COST_TO_ACCESS:
            return jsonify({'error': 'Insufficient credits'}), 403

        # Update expired listings
        update_listing_status(session, Scholarship)

        # Deduct credits
        user.credits -= COST_TO_ACCESS
        session.commit()

        # Get search and filter parameters
        title = request.args.get('title')
        organization = request.args.get('organization')
        min_amount = request.args.get('min_amount', type=int)
        max_amount = request.args.get('max_amount', type=int)
        include_expired = request.args.get('include_expired', 'false').lower() == 'true'
        
        # Start the base query
        query = session.query(Scholarship)

        # Only show active listings by default
        if not include_expired:
            query = query.filter(Scholarship.status == ListingStatus.ACTIVE)

        # Apply other filters
        if title:
            query = query.filter(Scholarship.title.ilike(f"%{title}%"))
        if organization:
            query = query.join(Organization).filter(Organization.name.ilike(f"%{organization}%"))
        if min_amount is not None:
            query = query.filter(Scholarship.amount >= min_amount)
        if max_amount is not None:
            query = query.filter(Scholarship.amount <= max_amount)

        # Apply ordering
        order_by = request.args.get('order_by', 'deadline')
        if order_by == 'deadline':
            query = query.order_by(Scholarship.deadline.asc())
        elif order_by == 'newest':
            query = query.order_by(Scholarship.created_at.desc())

        results = query.all()

        return jsonify({
            'credits': user.credits,
            'scholarships': [{
                'id': scholarship.scholarship_id,
                'title': scholarship.title,
                'description': scholarship.description,
                'organization': scholarship.organization.name if scholarship.organization else None,
                'amount': scholarship.amount,
                'deadline': scholarship.deadline.isoformat(),
                'status': scholarship.status.value,
                'created_at': scholarship.created_at.isoformat()
            } for scholarship in results]
        })
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@scholarships_internships.route('/internships/search', methods=['GET'])
@login_required
def internship_ordering_date():
    session = Session()
    try:
        user = session.query(User).filter_by(user_id=current_user.user_id).first()

        # Check if user has enough credits
        if user.credits < COST_TO_ACCESS:
            return jsonify({'error': 'Insufficient credits'}), 403

        # Update expired listings
        update_listing_status(session, Internship)

        # Deduct credits
        user.credits -= COST_TO_ACCESS
        session.commit()

        # Get search and filter parameters
        title = request.args.get('title')
        organization = request.args.get('organization')
        min_amount = request.args.get('min_amount', type=int)
        max_amount = request.args.get('max_amount', type=int)
        include_expired = request.args.get('include_expired', 'false').lower() == 'true'
        
        # Start the base query
        query = session.query(Internship)

        # Only show active listings by default
        if not include_expired:
            query = query.filter(Internship.status == ListingStatus.ACTIVE)

        # Apply other filters
        if title:
            query = query.filter(Internship.title.ilike(f"%{title}%"))
        if organization:
            query = query.join(Organization).filter(Organization.name.ilike(f"%{organization}%"))
        if min_amount is not None:
            query = query.filter(Internship.amount >= min_amount)
        if max_amount is not None:
            query = query.filter(Internship.amount <= max_amount)

        # Apply ordering
        order_by = request.args.get('order_by', 'deadline')
        if order_by == 'deadline':
            query = query.order_by(Internship.deadline.asc())
        elif order_by == 'newest':
            query = query.order_by(Internship.created_at.desc())

        results = query.all()

        return jsonify({
            'credits': user.credits,
            'internships': [{
                'id': internship.internship_id,
                'title': internship.title,
                'description': internship.description,
                'organization': internship.organization.name if internship.organization else None,
                'amount': internship.amount,
                'deadline': internship.deadline.isoformat(),
                'status': internship.status.value,
                'created_at': internship.created_at.isoformat()
            } for internship in results]
        })
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


# Function for deleting scholarships and internships
def delete_listing(listing_type: str, listing_id: int, user_id: int, session) -> tuple[bool, Optional[str]]:
    """
    Delete a scholarship or internship listing
    
    Args:
        listing_type: Either 'scholarship' or 'internship'
        listing_id: ID of the listing to delete
        user_id: ID of the user attempting to delete
        session: SQLAlchemy session
        
    Returns:
        Tuple of (success: bool, error_message: Optional[str])
    """
    try:
        Model = Scholarship if listing_type == 'scholarship' else Internship
        listing = session.query(Model).get(listing_id)
        
        if not listing:
            return False, f"{listing_type.title()} not found"
            
        success, error = listing.safe_delete(session, user_id)
        if success:
            session.commit()
            
        return success, error
        
    except Exception as e:
        session.rollback()
        return False, f"Error during deletion: {str(e)}"

# Deleting scholarships and internships
@scholarships_internships.route('/api/<listing_type>/<int:listing_id>', methods=['DELETE'])
@login_required
def delete_listing_route(listing_type, listing_id):
    success, error = delete_listing(
        listing_type=listing_type,
        listing_id=listing_id,
        user_id=current_user.user_id,
        session= Session()
    )
    
    if success:
        return jsonify({'message': f'{listing_type.title()} deleted successfully'}), 200
    else:
        return jsonify({'error': error}), 400