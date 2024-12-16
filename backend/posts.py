# posts.py
# Replaces global sessions with current_app.session_factory().
# Every database query uses s = current_app.session_factory() for consistency.

from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from sqlalchemy import func
from .database.create import Follow, Post, User, Vote, Comment
from .config import COST_TO_ACCESS, REWARD_FOR_POSTING
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/post', methods=['POST'])
@login_required
def add_post():
    s = current_app.session_factory()
    data = request.get_json()
    if not data or 'content' not in data or 'title' not in data:
        return jsonify({'error': 'Content is required'}), 400

    # Create and commit new post
    new_post = Post(user_id=current_user.user_id, content=data['content'], title=data["title"])
    s.add(new_post)
    try:
        s.commit()
        # Reward user after successful post creation
        current_user.credits += REWARD_FOR_POSTING
        s.commit()
    except Exception as e:
        s.rollback()
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Post added', 'post': {'id': new_post.post_id, 'content': new_post.content}}), 201

@posts_bp.route('/posts', methods=['GET'])
@login_required
def get_posts():
    s = current_app.session_factory()
    try:
        user = s.query(User).filter_by(user_id=current_user.user_id).first()
        if user.credits < COST_TO_ACCESS:
            return jsonify({"error": "Insufficient credits"}), 403

        posts = s.query(Post).all()
        # Deduct credits for access
        user.credits -= COST_TO_ACCESS
        s.commit()

        return jsonify({'posts': [
            {
                'id': post.post_id,
                'author': post.user.name,
                'content': post.content,
                'title': post.title,
                'created_at': post.created_at,
                'author_id': post.user_id,
            } for post in posts]}), 200
    except SQLAlchemyError as e:
        s.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500

def get_post(post_id):
    s = current_app.session_factory()
    post = s.query(Post).filter_by(post_id=post_id).first()
    if not post:
        return jsonify({"error": "Post not found"}), 404

    # Count votes and check if current_user voted
    upvotes = s.query(Vote).filter_by(post_id=post_id, vote_type="upvote").count()
    downvotes = s.query(Vote).filter_by(post_id=post_id, vote_type="downvote").count()
    user_has_upvoted = s.query(Vote).filter_by(post_id=post_id, user_id=current_user.user_id, vote_type="upvote").first() is not None
    user_has_downvoted = s.query(Vote).filter_by(post_id=post_id, user_id=current_user.user_id, vote_type="downvote").first() is not None

    comments = s.query(Comment).filter_by(post_id=post_id).all()
    return jsonify({
        "post": {
            "id": post.post_id,
            "title": post.title,
            "content": post.content,
            "image_url": post.image_url,
            "created_at": post.created_at,
            "user": {
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
                "comment_id": c.comment_id,
                "comment_text": c.comment_text,
                "created_at": c.created_at,
                "user": {
                    "username": c.user.username,
                    "name": c.user.name,
                    "id": c.user.user_id,
                }
            } for c in comments
        ]
    })

@posts_bp.route("/post/<int:post_id>")
def fetch_post(post_id):
    return get_post(post_id)

@posts_bp.route('/post/<int:post_id>', methods=['DELETE'])
@login_required
def delete_post(post_id):
    s = current_app.session_factory()
    try:
        post = s.query(Post).filter_by(post_id=post_id).first()
        if not post:
            return jsonify({"error": "Post not found"}), 404

        # Only allow owners to delete
        if post.user_id != current_user.user_id:
            return jsonify({"error": "Unauthorized: You can only delete your own posts"}), 403

        s.delete(post)
        s.commit()
        return jsonify({"message": "Post deleted successfully"}), 200
    except SQLAlchemyError as e:
        s.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500

@posts_bp.route('/posts/<int:user_id>', methods=['GET'])
@login_required
def get_user_posts(user_id):
    s = current_app.session_factory()
    posts = s.query(Post).filter(Post.user_id == user_id).all()
    post_list = []
    for p in posts:
        author = s.query(User).filter(User.user_id == p.user_id).first()
        post_list.append({
            'id': p.post_id,
            'title': p.title,
            'content': p.content,
            'author': author.name if author else 'Unknown',
            'created_at': p.created_at,
            'author_id': p.user_id,
        })
    return jsonify({'posts': post_list}), 200

@posts_bp.route('/posts/sorted_by_date', methods=['GET'])
@login_required
def get_posts_sorted_by_date():
    s = current_app.session_factory()
    posts = s.query(Post).order_by(Post.created_at.desc()).all()
    post_list = []
    for p in posts:
        author = s.query(User).filter(User.user_id == p.user_id).first()
        post_list.append({
            'id': p.post_id,
            'title': p.title,
            'content': p.content,
            'author': author.name if author else 'Unknown',
            'created_at': p.created_at
        })
    return jsonify({'posts': post_list}), 200

@posts_bp.route('/posts/sorted_by_votes', methods=['GET'])
@login_required
def get_posts_sorted_by_votes():
    s = current_app.session_factory()
    posts_with_votes = s.query(
        Post,
        func.count(Vote.vote_id).label('vote_count')
    ).join(Vote, Vote.post_id == Post.post_id, isouter=True) \
     .group_by(Post.post_id) \
     .order_by(func.count(Vote.vote_id).desc()).all()

    post_list = []
    for p, vote_count in posts_with_votes:
        author = s.query(User).filter(User.user_id == p.user_id).first()
        post_list.append({
            'id': p.post_id,
            'title': p.title,
            'content': p.content,
            'author': author.name if author else 'Unknown',
            'vote_count': vote_count,
            'created_at': p.created_at
        })
    return jsonify({'posts': post_list}), 200

@posts_bp.route('/posts/followed', methods=['GET'])
@login_required
def get_posts_of_followed_users():
    s = current_app.session_factory()
    followed_user_ids = s.query(Follow.followed_id).filter(Follow.follower_id == current_user.user_id).all()
    followed_user_ids = [fid[0] for fid in followed_user_ids]

    posts = s.query(Post).filter(Post.user_id.in_(followed_user_ids)).all()
    post_list = []
    for p in posts:
        author = s.query(User).filter(User.user_id == p.user_id).first()
        post_list.append({
            'id': p.post_id,
            'title': p.title,
            'content': p.content,
            'author': author.name if author else 'Unknown',
            'created_at': p.created_at
        })
    return jsonify({'posts': post_list}), 200

@posts_bp.route('/post/<int:post_id>/vote', methods=['POST'])
@login_required
def add_vote(post_id):
    s = current_app.session_factory()
    data = request.get_json()
    if not data or data.get('vote_type') not in ['upvote', 'downvote']:
        return jsonify({'error': 'Vote type must be "upvote" or "downvote"'}), 400

    try:
        post = s.query(Post).filter_by(post_id=post_id).first()
        if not post:
            return jsonify({'error': 'Post not found'}), 404

        existing_vote = s.query(Vote).filter_by(post_id=post_id, user_id=current_user.user_id).first()
        if existing_vote:
            # Update or remove existing vote
            if existing_vote.vote_type != data['vote_type']:
                existing_vote.vote_type = data['vote_type']
                action = 'updated'
            else:
                s.delete(existing_vote)
                action = 'removed'
        else:
            # Add new vote
            new_vote = Vote(post_id=post_id, user_id=current_user.user_id, vote_type=data['vote_type'])
            s.add(new_vote)
            action = 'added'

        s.commit()
        return jsonify({'message': f'Vote {action} successfully'}), 200
    except SQLAlchemyError as e:
        s.rollback()
        return jsonify({'error': str(e)}), 500

@posts_bp.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def comment_on_post(post_id):
    s = current_app.session_factory()
    try:
        data = request.get_json()
        comment_text = data.get('comment_text')
        if not comment_text:
            return jsonify({"error": "Comment text is required"}), 400

        post = s.query(Post).filter_by(post_id=post_id).first()
        if not post:
            return jsonify({"error": "Post not found"}), 404

        new_comment = Comment(
            post_id=post_id,
            user_id=current_user.user_id,
            comment_text=comment_text,
            created_at=datetime.utcnow()
        )
        s.add(new_comment)
        s.commit()
        return jsonify({"message": "Comment added successfully"}), 201
    except SQLAlchemyError as e:
        s.rollback()
        return jsonify({"error": str(e)}), 500

@posts_bp.route('/posts/<int:post_id>/votes', methods=['GET'])
@login_required
def get_votes(post_id):
    s = current_app.session_factory()
    upvotes_count = s.query(Vote).filter(Vote.post_id == post_id, Vote.vote_type == 'upvote').count()
    downvotes_count = s.query(Vote).filter(Vote.post_id == post_id, Vote.vote_type == 'downvote').count()

    return jsonify({'post_id': post_id, 'upvotes': upvotes_count, 'downvotes': downvotes_count}), 200

@posts_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
@login_required
def get_comments(post_id):
    s = current_app.session_factory()
    comments = s.query(Comment).filter(Comment.post_id == post_id).all()
    comment_list = [{
        'id': c.comment_id,
        'user_id': c.user_id,
        'comment_text': c.comment_text,
        'created_at': c.created_at
    } for c in comments]

    return jsonify({'post_id': post_id, 'comments': comment_list}), 200

@posts_bp.route('/get_credits', methods=['GET'])
@login_required
def get_credits():
    # current_user is loaded by flask_login and has credits
    return jsonify({'credits': current_user.credits})

def delete_vote(post_id: int, user_id: int, s, Post, Vote):
    # Helper function to delete a user's vote on a post
    try:
        post = s.query(Post).get(post_id)
        if not post:
            return False, "Post not found", 404

        vote = s.query(Vote).filter(Vote.post_id == post_id, Vote.user_id == user_id).first()
        if not vote:
            return False, "Vote not found", 404

        s.delete(vote)
        s.commit()
        return True, "Vote deleted successfully", 200
    except SQLAlchemyError as e:
        s.rollback()
        return False, str(e), 500

def get_post_votes(post_id: int, s, Post, Vote):
    # Helper to count votes for a post
    upvotes = s.query(Vote).filter(Vote.post_id == post_id, Vote.vote_type == 'upvote').count()
    downvotes = s.query(Vote).filter(Vote.post_id == post_id, Vote.vote_type == 'downvote').count()
    return {'upvotes': upvotes, 'downvotes': downvotes, 'total': upvotes - downvotes}

@posts_bp.route('/posts/<int:post_id>/vote', methods=['DELETE'])
@login_required
def remove_vote(post_id: int):
    s = current_app.session_factory()
    success, message, status_code = delete_vote(post_id, current_user.user_id, s, Post, Vote)
    if not success:
        return jsonify({'error': message}), status_code

    vote_counts = get_post_votes(post_id, s, Post, Vote)
    return jsonify({'message': message, 'votes': vote_counts}), status_code
