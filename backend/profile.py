from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from .database.create import User, engine, User, Follow
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy import and_ 


profile = Blueprint('profile', __name__)
# Create a new session factory
Session = sessionmaker(bind=engine)





@profile.route('/profile', methods=['POST'])
@login_required  # Ensures that only logged-in users can update profiles
def update_profile():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    session = Session()
    user = session.query(User).get(current_user.user_id)  # Fetch user from the database
    if user is None:
        return jsonify({"error": "User not found"}), 404

    # Update the user's profile attributes if provided in the request
    user.bio = data.get('bio', user.bio)
    user.name = data.get('name', user.name)

    # Commit the changes to the database
    try:
        session.commit()
    except Exception as e:
        session.rollback()  # Rollback in case of error
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "success": "Profile updated successfully",
        "updated_profile": {
            'id': user.user_id,
            'email': user.email,
            'name': user.name,
            'bio': user.bio,
            'company': user.company,
            'role': user.role,
            'school': user.school,
        }
    })




@profile.route('/profile', methods=['GET'])
@login_required
def get_followings():
    # Fetch the current user's profile information from the database
    user = current_user
    if user is None:
        return jsonify({"error": "User not found"}), 404

    # Get the users the current user is following
    following_alias = aliased(User)  # Alias for the User table
    followings = Session().query(following_alias).join(Follow, Follow.follower_id == user.user_id).filter(
        Follow.follower_id == user.user_id).all()

    print(f"User availability: {user.mentorship_availability}")
    # Return only followings
    return jsonify({
        'id': user.user_id,
        'email': user.email,
        'name': user.name,
        'bio': user.bio or 'No bio available',  # Default message if bio is None
        'followings': [following.name for following in followings],
        'mentorship_availability': 'yes' if user.mentorship_availability else 'no'
    })

@profile.route('/profile/<int:user_id>', methods=['GET'])
@login_required
def get_others_profile(user_id):
    # Fetch the current user's profile information from the database
    session = Session()
    user = session.query(User).filter_by(user_id=user_id).first()
    if user is None:
        return jsonify({"error": "User not found"}), 404

    # Get the users the current user is following
    following_alias = aliased(User)  # Alias for the User table
    followings = Session().query(following_alias).join(Follow, Follow.follower_id == user.user_id).filter(
        Follow.follower_id == user.user_id).all()

    # Return only followings
    return jsonify({
        'id': user.user_id,
        'email': user.email,
        'name': user.name,
        'bio': user.bio or 'No bio available',  # Default message if bio is None
        'followings': [following.name for following in followings]
    })

@profile.route('/follow', methods=['POST'])
@login_required
def follow_user():
    data = request.get_json()
    if not data or 'user_id' not in data:
        return jsonify({"error": "Missing user_id in request"}), 400
    
    target_user_id = data['user_id']
    session = Session()
    
    # Check if target user exists
    target_user = session.query(User).get(target_user_id)
    if not target_user:
        return jsonify({"error": "Target user not found"}), 404
    
    # Prevent self-following
    if target_user_id == current_user.user_id:
        return jsonify({"error": "Cannot follow yourself"}), 400
    
    # Check if already following
    existing_follow = session.query(Follow).filter(
        and_(
            Follow.follower_id == current_user.user_id,
            Follow.followed_id == target_user_id
        )
    ).first()
    
    if existing_follow:
        return jsonify({"error": "Already following this user"}), 400
    
    # Create new follow relationship
    try:
        new_follow = Follow(
            follower_id=current_user.user_id,
            followed_id=target_user_id
        )
        session.add(new_follow)
        session.commit()
        
        return jsonify({
            "success": "Successfully followed user",
            "following": {
                "user_id": target_user_id,
                "name": target_user.name
            }
        })
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@profile.route('/unfollow', methods=['POST'])
@login_required
def unfollow_user():
    data = request.get_json()
    if not data or 'user_id' not in data:
        return jsonify({"error": "Missing user_id in request"}), 400
    
    target_user_id = data['user_id']
    session = Session()
    
    # Check if target user exists
    target_user = session.query(User).get(target_user_id)
    if not target_user:
        return jsonify({"error": "Target user not found"}), 404
    
    # Find and remove the follow relationship
    follow = session.query(Follow).filter(
        and_(
            Follow.follower_id == current_user.user_id,
            Follow.followed_id == target_user_id
        )
    ).first()
    
    if not follow:
        return jsonify({"error": "Not following this user"}), 400
    
    try:
        session.delete(follow)
        session.commit()
        
        return jsonify({
            "success": "Successfully unfollowed user",
            "unfollowed": {
                "user_id": target_user_id,
                "name": target_user.name
            }
        })
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()