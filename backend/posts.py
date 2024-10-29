from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user

# Define the blueprint
posts_bp = Blueprint('posts', __name__)

# In-memory "database" for posts
posts_db = []


# Endpoint to add a new post
@posts_bp.route('/post', methods=['POST'])
@login_required
def add_post():
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({'error': 'Content is required'}), 400

    post = {
        'author': current_user.id,
        'content': data['content']
    }
    posts_db.append(post)
    return jsonify({'message': 'Post added', 'post': post}), 201


# Endpoint to fetch all posts
@posts_bp.route('/posts', methods=['GET'])
@login_required
def get_posts():
    return jsonify({'posts': posts_db}), 200
