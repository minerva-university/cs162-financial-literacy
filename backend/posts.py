from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func
from .database.create import Follow, Post, User, Vote, engine
from sqlalchemy.orm import sessionmaker
from config import (
    COST_TO_ACCESS,
    REWARD_FOR_POSTING,
)

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
        # Reward the user for posting
        user_id.credits += REWARD_FOR_POSTING
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
    # Fetch all posts from the database if the credit balance is sufficient
    if user_id.credits >= COST_TO_ACCESS:
        user_id.credits -= COST_TO_ACCESS
        session.commit()
        posts = session.query(Post).all()  # Retrieve all posts
        return jsonify({'posts': [{'id': post.post_id, 'author': post.user_id, 'content': post.content} for post in posts]}), 200
    else:
        return jsonify({'error': 'Insufficient credits'}), 403

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

# adding votes, upvotes/downvotes
@posts_bp.route('/post/<int:post_id>/vote', methods=['POST'])
@login_required
def add_vote(post_id):
    data = request.get_json()
    if not data or 'vote_type' not in data or data['vote_type'] not in ['upvote', 'downvote']:
        return jsonify({'error': 'Vote type is required and must be "upvote" or "downvote"'}), 400

    session = Session()

    # Check if the user has already voted on this post
    existing_vote = session.query(Vote).filter(
        Vote.post_id == post_id,
        Vote.user_id == current_user.user_id
    ).first()

    if existing_vote:
        # Update the existing vote
        existing_vote.vote_type = data['vote_type']
        action = 'updated'
    else:
        # Add a new vote
        new_vote = Vote(
            post_id=post_id,
            user_id=current_user.user_id,
            vote_type=data['vote_type']
        )
        session.add(new_vote)
        action = 'added'

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': f'Vote {action} successfully'}), 200


# commenting on a post
@posts_bp.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    data = request.get_json()
    if not data or 'comment_text' not in data:
        return jsonify({'error': 'Comment text is required'}), 400

    session = Session()

    # Create a new comment for the post
    new_comment = Comment(
        post_id=post_id,
        user_id=current_user.user_id,
        comment_text=data['comment_text']
    )

    session.add(new_comment)
    
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Comment added successfully', 'comment': {'id': new_comment.comment_id, 'text': new_comment.comment_text}}), 201


# fetching votes of a post
@posts_bp.route('/post/<int:post_id>/votes', methods=['GET'])
@login_required
def get_votes(post_id):
    session = Session()

    # Count the number of upvotes and downvotes for the post
    upvotes_count = session.query(Vote).filter(
        Vote.post_id == post_id,
        Vote.vote_type == 'upvote'
    ).count()

    downvotes_count = session.query(Vote).filter(
        Vote.post_id == post_id,
        Vote.vote_type == 'downvote'
    ).count()

    return jsonify({
        'post_id': post_id,
        'upvotes': upvotes_count,
        'downvotes': downvotes_count
    }), 200


# fetching comments of a post
@posts_bp.route('/post/<int:post_id>/comments', methods=['GET'])
@login_required
def get_comments(post_id):
    session = Session()

    # Fetch all comments for the post
    comments = session.query(Comment).filter(Comment.post_id == post_id).all()

    # Return the list of comments
    comment_list = [{
        'id': comment.comment_id,
        'user_id': comment.user_id,
        'comment_text': comment.comment_text,
        'created_at': comment.created_at
    } for comment in comments]

    return jsonify({'post_id': post_id, 'comments': comment_list}), 200


# Endpoint to fetch the number of credits available to the user
@posts_bp.route('/get_credits', methods=['GET'])
@login_required
def get_credits():
    user = current_user
    return jsonify({'credits': user.credits})
