from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from .database.create import Post, engine
from sqlalchemy.orm import sessionmaker

# Define the blueprint
posts_bp = Blueprint('posts', __name__)
Session = sessionmaker(bind=engine)

# Endpoint to add a new post
@posts_bp.route('/post', methods=['POST'])
@login_required
def add_post():

    data = request.get_json()
    if not data or 'content' not in data or 'title' not in data:
        return jsonify({'error': 'Content is required'}), 400

    session = Session()

    # Create a new post instance and associate it with the current user
    new_post = Post(
        user_id=current_user.user_id,  # Assuming author_id is a foreign key to the User model
        content=data['content'],
        title=data["title"]
    )

    # Add the new post to the database
    session.add(new_post)
    try:
        session.commit()
    except Exception as e:
        session.rollback()  # Rollback in case of an error
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Post added', 'post': {'id': new_post.post_id, 'content': new_post.content}}), 201


# Endpoint to fetch all posts
@posts_bp.route('/posts', methods=['GET'])
@login_required
def get_posts():
    session = Session()
    # Fetch all posts from the database
    posts = session.query(Post).all()  # Retrieve all posts
    return jsonify({'posts': [{'id': post.post_id, 'author': post.user_id, 'content': post.content} for post in posts]}), 200
