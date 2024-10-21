from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

profile = Blueprint('profile', __name__)

@profile.route('/profile', methods=['GET'])
#@login_required
def get_profile():
    # Return the current user's profile information
    return jsonify({
        'id': current_user.id,
        'email': current_user.get('email'),
        'name': current_user.get('name'),
        'bio': current_user.get('bio', 'No bio available')
    })

@profile.route('/profile', methods=['POST'])
#@login_required  # Ensures that only logged-in users can update profiles
def update_profile():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    current_user['bio'] = data.get('bio', current_user.get('bio', 'No bio available'))
    current_user['name'] = data.get('name', current_user.get('name'))

    # Update the user dictionary directly (in-memory)
    return jsonify({
        "success": "Yes",
        "updated_profile": {
            'id': current_user.id,
            'email': current_user.get('email'),
            'name': current_user.get('name'),
            'bio': current_user.get('bio')
        }
    })
