from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from .database.create import User, engine
from sqlalchemy.orm import sessionmaker


profile = Blueprint('profile', __name__)
# Create a new session factory
Session = sessionmaker(bind=engine)


@profile.route('/profile', methods=['GET'])
@login_required
def get_profile():
    # Fetch the current user's profile information from the database
    user = current_user
    if user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        'id': user.user_id,
        'email': user.email,
        'name': user.name,
        'bio': user.bio or 'No bio available'  # Default message if bio is None
    })


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
            'bio': user.bio
        }
    })

from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from sqlalchemy.orm import aliased
from .database.create import Session, User, Follow

profile = Blueprint('profile', __name__)

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

    # Return only followings
    return jsonify({
        'id': user.user_id,
        'email': user.email,
        'name': user.name,
        'bio': user.bio or 'No bio available',  # Default message if bio is None
        'followings': [following.name for following in followings]
    })

@profile.route('/profile', methods=['GET'])
@login_required
def get_followers():
    # Fetch the current user's profile information from the database
    user = current_user
    if user is None:
        return jsonify({"error": "User not found"}), 404

    # Get the users who are following the current user
    follower_alias = aliased(User)  # Alias for the User table
    followers = Session().query(follower_alias).join(Follow, Follow.followed_id == user.user_id).filter(
        Follow.followed_id == user.user_id).all()

    # Return only followers
    return jsonify({
        'id': user.user_id,
        'email': user.email,
        'name': user.name,
        'bio': user.bio or 'No bio available',  # Default message if bio is None
        'followers': [follower.name for follower in followers]
    })

