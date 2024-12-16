# profile.py
# Similarly uses current_app.session_factory() instead of global sessions.
# Each route obtains a session on-demand.

from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user
from .database.create import User, Follow
from sqlalchemy.orm import aliased
from sqlalchemy import and_

profile = Blueprint('profile', __name__)

# Update Profile
@profile.route('/profile', methods=['POST'])
@login_required
def update_profile():
    s = current_app.session_factory()
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    user = s.query(User).get(current_user.user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    # Update user attributes if provided
    user.bio = data.get('bio', user.bio)
    user.name = data.get('name', user.name)

    try:
        s.commit()
    except Exception as e:
        s.rollback()
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
    s = current_app.session_factory()
    user = s.query(User).filter_by(user_id=current_user.user_id).first()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    # Get the users the current user is following
    following_alias = aliased(User)
    followings = s.query(following_alias).join(Follow, Follow.followed_id == following_alias.user_id) \
                    .filter(Follow.follower_id == user.user_id).all()
    return jsonify({
        'id': user.user_id,
        'email': user.email,
        'name': user.name,
        'bio': user.bio or 'No bio available',
        'followings': [f.name for f in followings],
        'credits': user.credits,
        'mentorship_availability': 'yes' if user.mentorship_availability else 'no'
    })

# Update Bio
@profile.route('/profile/update_bio', methods=['POST'])
@login_required
def update_bio():
    s = current_app.session_factory()
    data = request.get_json()

    bio = data.get('bio')
    if not bio:
        return jsonify({"error": "Bio cannot be empty"}), 400

    user = s.query(User).get(current_user.user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        user.bio = bio
        s.commit()
        return jsonify({"success": True, "message": "Bio updated successfully", "bio": user.bio})
    except Exception as e:
        s.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        s.close()


@profile.route('/profile/<int:user_id>', methods=['GET'])
@login_required
def get_others_profile(user_id):
    s = current_app.session_factory()
    user = s.query(User).filter_by(user_id=user_id).first()
    if user is None:
        return jsonify({"error": "User not found"}), 404

    following_alias = aliased(User)
    followings = s.query(following_alias).join(Follow, Follow.followed_id == following_alias.user_id) \
                    .filter(Follow.follower_id == user.user_id).all()

    return jsonify({
        'id': user.user_id,
        'email': user.email,
        'name': user.name,
        'bio': user.bio or 'No bio available',  # Default message if bio is None
        'followings': [f.name for f in followings],
        'mentorship_availability': 'yes' if user.mentorship_availability else 'no'
    })

@profile.route('/follow', methods=['POST'])
@login_required
def follow_user():
    s = current_app.session_factory()
    data = request.get_json()
    if not data or 'user_id' not in data:
        return jsonify({"error": "Missing user_id in request"}), 400

    target_user_id = data['user_id']
    target_user = s.query(User).get(target_user_id)
    if not target_user:
        return jsonify({"error": "Target user not found"}), 404

    if target_user_id == current_user.user_id:
        return jsonify({"error": "Cannot follow yourself"}), 400

    existing_follow = s.query(Follow).filter(
        and_(Follow.follower_id == current_user.user_id, Follow.followed_id == target_user_id)
    ).first()

    if existing_follow:
        return jsonify({"error": "Already following this user"}), 400

    try:
        new_follow = Follow(follower_id=current_user.user_id, followed_id=target_user_id)
        s.add(new_follow)
        s.commit()
        return jsonify({
            "success": "Successfully followed user",
            "following": {
                "user_id": target_user_id,
                "name": target_user.name
            }
        })
    except Exception as e:
        s.rollback()
        return jsonify({"error": str(e)}), 500

@profile.route('/unfollow', methods=['POST'])
@login_required
def unfollow_user():
    s = current_app.session_factory()
    data = request.get_json()
    if not data or 'user_id' not in data:
        return jsonify({"error": "Missing user_id in request"}), 400

    target_user_id = data['user_id']
    target_user = s.query(User).get(target_user_id)
    if not target_user:
        return jsonify({"error": "Target user not found"}), 404

    follow = s.query(Follow).filter(
        and_(Follow.follower_id == current_user.user_id, Follow.followed_id == target_user_id)
    ).first()

    if not follow:
        return jsonify({"error": "Not following this user"}), 400

    try:
        s.delete(follow)
        s.commit()
        return jsonify({
            "success": "Successfully unfollowed user",
            "unfollowed": {
                "user_id": target_user_id,
                "name": target_user.name
            }
        })
    except Exception as e:
        s.rollback()
        return jsonify({"error": str(e)}), 500
