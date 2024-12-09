from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func
from .database.create import Follow, Post, User, Vote, Comment, engine
from sqlalchemy.orm import sessionmaker
from .config import COST_TO_ACCESS, REWARD_FOR_POSTING
from sqlalchemy.exc import IntegrityError
from typing import Tuple, Optional
from datetime import datetime, timezone


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
        current_user.credits += REWARD_FOR_POSTING
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
    if current_user.credits >= COST_TO_ACCESS:
        current_user.credits -= COST_TO_ACCESS
        session.commit()
        posts = session.query(Post).all()  # Retrieve all posts
        return jsonify({
            'posts': [
                {'id': post.post_id,
                 'author': post.user.name,
                 'content': post.content,
                 'title': post.title,
                 'created_at':post.created_at} for post in posts
                ]}), 200
    else:
        return jsonify({'error': 'Insufficient credits'}), 403

def get_post(post_id):
    """Fetches a post with its upvotes, downvotes, and comments.

    Args:
        post_id (int): ID of the post to fetch.

    Returns:
        dict: Dictionary containing post information, upvotes, downvotes, and comments.
    """

    session = Session()

    # Fetch the post
    post = session.query(Post).filter_by(post_id=post_id).first()

    if not post:
        return jsonify({"error": "Post not found"}), 404

    # Calculate upvotes and downvotes, checking if current user has voted
    upvotes = session.query(Vote).filter_by(post_id=post_id, vote_type="upvote").count()
    downvotes = session.query(Vote).filter_by(post_id=post_id, vote_type="downvote").count()
    user_has_upvoted = session.query(Vote).filter_by(post_id=post_id, user_id=current_user.user_id, vote_type="upvote").first() is not None
    user_has_downvoted = session.query(Vote).filter_by(post_id=post_id, user_id=current_user.user_id, vote_type="downvote").first() is not None

    # Fetch comments for the post
    comments = session.query(Comment).filter_by(post_id=post_id).all()

    # Format response data
    response = {
        "post": {
            "id": post.post_id,
            "title": post.title,
            "content": post.content,
            "image_url": post.image_url,
            "created_at": post.created_at,
            "user": {  # Include user details if needed
                "username": post.user.username,
                "name": post.user.name,
                "id": post.user.user_id,
            }
        },
        "upvotes": upvotes,
        "downvotes": downvotes,
        "user_has_upvoted": user_has_upvoted,
        "user_has_downvoted": user_has_downvoted,
        "comments": [
            {
                "comment_id": comment.comment_id,
                "comment_text": comment.comment_text,
                "created_at": comment.created_at,
                "user": {  # Include user details if needed
                    "username": comment.user.username,
                    "name": comment.user.name,
                    "id": comment.user.user_id,
                }
            }
            for comment in comments
        ]
    }

    session.close()
    return jsonify(response)


# Register the endpoint with your Flask app
@posts_bp.route("/post/<int:post_id>")
def fetch_post(post_id):
    return get_post(post_id)

# Endpoint to delete a post
@posts_bp.route('/post/<int:post_id>', methods=['DELETE'])
@login_required
def delete_post(post_id):
    session = Session()

    # Fetch the post to delete
    post = session.query(Post).filter_by(post_id=post_id).first()

    if not post:
        return jsonify({'error': 'Post not found'}), 404

    # Check if the current user is the owner of the post
    if post.user_id != current_user.user_id:
        return jsonify({'error': 'Unauthorized: You can only delete your own posts'}), 403

    try:
        # Delete the post
        session.delete(post)
        session.commit()
        return jsonify({'message': 'Post deleted successfully'}), 200
    except Exception as e:
        session.rollback()  # Rollback in case of an error
        return jsonify({'error': 'An error occurred while deleting the post', 'details': str(e)}), 500



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
        if existing_vote.vote_type != data['vote_type']:
            # Update the existing vote
            existing_vote.vote_type = data['vote_type']
            action = 'updated'
        else:
            delete_vote(
                post_id=post_id,
                user_id=current_user.user_id,
                session=Session(),
                Post=Post,
                Vote=Vote
            )
            action = 'deleted'

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

    return jsonify({'message': 'Comment added successfully', 'comment': {'id': new_comment.comment_id, 'created_at':new_comment.created_at,"user_id":current_user.user_id, "name":current_user.name, 'text': new_comment.comment_text}}), 201


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

# Function for removing votes
def delete_vote(
    post_id: int,
    user_id: int,
    session,
    Post,
    Vote
) -> Tuple[bool, Optional[str], int]:
    """
    Delete a user's vote on a post
    
    Args:
        post_id: ID of the post
        user_id: ID of the user who made the vote
        session: SQLAlchemy session
        Post: Post model class
        Vote: Vote model class
    
    Returns:
        Tuple of (success: bool, error_message: Optional[str], status_code: int)
    """
    try:
        # Check if post exists
        post = session.query(Post).get(post_id)
        if not post:
            return False, "Post not found", 404

        # Find the vote
        vote = session.query(Vote).filter(
            Vote.post_id == post_id,
            Vote.user_id == user_id
        ).first()

        if not vote:
            return False, "Vote not found", 404

        # Delete the vote
        session.delete(vote)
        session.commit()
        
        return True, "Vote deleted successfully", 200

    except IntegrityError as e:
        session.rollback()
        return False, "Database integrity error", 500
    except Exception as e:
        session.rollback()
        return False, f"Error deleting vote: {str(e)}", 500

def get_post_votes(
    post_id: int,
    session,
    Post,
    Vote
) -> dict:
    """
    Get vote counts for a post
    
    Args:
        post_id: ID of the post
        session: SQLAlchemy session
        Post: Post model class
        Vote: Vote model class
    
    Returns:
        Dict containing vote counts
    """
    upvotes = session.query(Vote).filter(
        Vote.post_id == post_id,
        Vote.vote_type == 'upvote'
    ).count()

    downvotes = session.query(Vote).filter(
        Vote.post_id == post_id,
        Vote.vote_type == 'downvote'
    ).count()

    return {
        'upvotes': upvotes,
        'downvotes': downvotes,
        'total': upvotes - downvotes
    }

# Route handler for deleting votes
@posts_bp.route('/post/<int:post_id>/vote', methods=['DELETE'])
@login_required
def remove_vote(post_id: int):
    """Delete a user's vote on a post"""
    
    # Process the vote deletion
    success, message, status_code = delete_vote(
        post_id=post_id,
        user_id=current_user.user_id,
        session=Session(),
        Post=Post,
        Vote=Vote
    )

    if not success:
        return jsonify({'error': message}), status_code

    # Get updated vote counts
    vote_counts = get_post_votes(
        post_id=post_id,
        session=Session(),
        Post=Post,
        Vote=Vote
    )

    return jsonify({
        'message': message,
        'votes': vote_counts
    }), status_code

