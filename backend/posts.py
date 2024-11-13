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

# Endpoint to fetch posts by a specific user
@posts_bp.route('/posts/<int:user_id>', methods=['GET'])
@login_required
def get_user_posts(user_id):
    session = Session()

    # Fetch posts made by a specific user
    posts = session.query(Post).filter(Post.user_id == user_id).all()
    post_list = []
    for post in posts:
        author = session.query(User).filter(User.user_id == post.user_id).first()
        post_list.append({
            'id': post.post_id,
            'title': post.title,
            'content': post.content,
            'author': author.name if author else 'Unknown',
            'created_at': post.created_at
        })
    
    return jsonify({'posts': post_list}), 200


# Endpoint to fetch posts sorted by date (descending by default)
@posts_bp.route('/posts/sorted_by_date', methods=['GET'])
@login_required
def get_posts_sorted_by_date():
    session = Session()

    # Fetch posts sorted by creation date (descending)
    posts = session.query(Post).order_by(Post.created_at.desc()).all()
    post_list = []
    for post in posts:
        author = session.query(User).filter(User.user_id == post.user_id).first()
        post_list.append({
            'id': post.post_id,
            'title': post.title,
            'content': post.content,
            'author': author.name if author else 'Unknown',
            'created_at': post.created_at
        })
    
    return jsonify({'posts': post_list}), 200


# Endpoint to fetch posts sorted by number of votes
@posts_bp.route('/posts/sorted_by_votes', methods=['GET'])
@login_required
def get_posts_sorted_by_votes():
    session = Session()

    # Fetch posts and count votes per post
    posts_with_votes = session.query(
        Post,
        func.count(Vote.vote_id).label('vote_count')
    ).join(Vote, Vote.post_id == Post.post_id, isouter=True) \
     .group_by(Post.post_id) \
     .order_by(func.count(Vote.vote_id).desc()).all()

    post_list = []
    for post, vote_count in posts_with_votes:
        author = session.query(User).filter(User.user_id == post.user_id).first()
        post_list.append({
            'id': post.post_id,
            'title': post.title,
            'content': post.content,
            'author': author.name if author else 'Unknown',
            'vote_count': vote_count,
            'created_at': post.created_at
        })
    
    return jsonify({'posts': post_list}), 200


# Endpoint to fetch posts of people the user follows
@posts_bp.route('/posts/followed', methods=['GET'])
@login_required
def get_posts_of_followed_users():
    session = Session()

    # Get the list of users that the current user follows
    followed_user_ids = session.query(Follow.followed_id) \
                               .filter(Follow.follower_id == current_user.user_id) \
                               .all()
    
    # Extract the followed user ids
    followed_user_ids = [followed_user_id[0] for followed_user_id in followed_user_ids]
    
    # Fetch posts from followed users
    posts = session.query(Post).filter(Post.user_id.in_(followed_user_ids)).all()
    
    post_list = []
    for post in posts:
        author = session.query(User).filter(User.user_id == post.user_id).first()
        post_list.append({
            'id': post.post_id,
            'title': post.title,
            'content': post.content,
            'author': author.name if author else 'Unknown',
            'created_at': post.created_at
        })
    
    return jsonify({'posts': post_list}), 200
