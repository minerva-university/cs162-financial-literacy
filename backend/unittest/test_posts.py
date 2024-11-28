import pytest
from flask import Flask
from flask_login import login_user, current_user
from unittest.mock import Mock, patch
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone

# Import the blueprint and models
from backend.posts import posts_bp  
from backend.database.create import Post, User, Vote, Comment, Follow


@pytest.fixture
def app():
    """Create a Flask app with the posts blueprint"""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    app.register_blueprint(posts_bp)
    return app

@pytest.fixture
def client(app):
    """Create a test client"""
    return app.test_client()

@pytest.fixture
def mock_session():
    """Create a mock SQLAlchemy session"""
    return Mock(spec=sessionmaker)

@pytest.fixture
def mock_current_user():
    """Create a mock current user"""
    user = Mock(spec=User)
    user.user_id = 1
    user.name = 'Test User'
    user.credits = 100
    return user

@pytest.fixture
def authenticated_client(client, mock_current_user):
    """Create an authenticated test client"""
    with patch('flask_login.current_user', mock_current_user):
        yield client

def test_add_post_success(authenticated_client, mock_current_user):
    """Test successful post creation"""
    post_data = {
        'content': 'Test post content',
        'title': 'Test Post Title'
    }
    
    with patch('flask_login.current_user', mock_current_user):
        response = authenticated_client.post('/post', 
            json=post_data,
            content_type='application/json'
        )
    
    assert response.status_code == 201
    assert response.json['message'] == 'Post added'
    assert 'post' in response.json
    assert 'id' in response.json['post']

def test_add_post_missing_content(authenticated_client):
    """Test post creation with missing content"""
    response = authenticated_client.post('/post', 
        json={'title': 'Incomplete Post'},
        content_type='application/json'
    )
    
    assert response.status_code == 400
    assert 'error' in response.json

def test_get_posts_sufficient_credits(authenticated_client, mock_current_user):
    """Test fetching posts when user has sufficient credits"""
    mock_current_user.credits = 50  # Ensure sufficient credits
    
    response = authenticated_client.get('/posts')
    
    assert response.status_code == 200
    assert 'posts' in response.json

def test_get_posts_insufficient_credits(authenticated_client, mock_current_user):
    """Test fetching posts when user has insufficient credits"""
    mock_current_user.credits = 0  # No credits
    
    response = authenticated_client.get('/posts')
    
    assert response.status_code == 403
    assert 'error' in response.json

def test_get_user_posts(authenticated_client):
    """Test fetching posts by a specific user"""
    response = authenticated_client.get('/posts/1')
    
    assert response.status_code == 200
    assert 'posts' in response.json

def test_add_vote_success(authenticated_client):
    """Test adding a vote to a post"""
    vote_data = {'vote_type': 'upvote'}
    
    response = authenticated_client.post('/post/1/vote', 
        json=vote_data,
        content_type='application/json'
    )
    
    assert response.status_code == 200
    assert 'message' in response.json

def test_add_vote_invalid_type(authenticated_client):
    """Test adding a vote with an invalid vote type"""
    vote_data = {'vote_type': 'invalid_vote'}
    
    response = authenticated_client.post('/post/1/vote', 
        json=vote_data,
        content_type='application/json'
    )
    
    assert response.status_code == 400
    assert 'error' in response.json

def test_add_comment_success(authenticated_client):
    """Test adding a comment to a post"""
    comment_data = {'comment_text': 'This is a test comment'}
    
    response = authenticated_client.post('/post/1/comment', 
        json=comment_data,
        content_type='application/json'
    )
    
    assert response.status_code == 201
    assert 'message' in response.json
    assert 'comment' in response.json

def test_add_comment_missing_text(authenticated_client):
    """Test adding a comment with missing text"""
    response = authenticated_client.post('/post/1/comment', 
        json={},
        content_type='application/json'
    )
    
    assert response.status_code == 400
    assert 'error' in response.json

def test_get_votes(authenticated_client):
    """Test fetching votes for a post"""
    response = authenticated_client.get('/post/1/votes')
    
    assert response.status_code == 200
    assert 'upvotes' in response.json
    assert 'downvotes' in response.json

def test_get_comments(authenticated_client):
    """Test fetching comments for a post"""
    response = authenticated_client.get('/post/1/comments')
    
    assert response.status_code == 200
    assert 'comments' in response.json
    assert 'post_id' in response.json

def test_get_credits(authenticated_client, mock_current_user):
    """Test fetching user credits"""
    mock_current_user.credits = 75
    
    response = authenticated_client.get('/get_credits')
    
    assert response.status_code == 200
    assert response.json['credits'] == 75

def test_delete_vote_success(authenticated_client):
    """Test deleting a user's vote"""
    response = authenticated_client.delete('/post/1/vote')
    
    assert response.status_code == 200
    assert 'message' in response.json
    assert 'votes' in response.json

def test_get_posts_sorted_by_date(authenticated_client):
    """Test fetching posts sorted by date"""
    response = authenticated_client.get('/posts/sorted_by_date')
    
    assert response.status_code == 200
    assert 'posts' in response.json

def test_get_posts_sorted_by_votes(authenticated_client):
    """Test fetching posts sorted by votes"""
    response = authenticated_client.get('/posts/sorted_by_votes')
    
    assert response.status_code == 200
    assert 'posts' in response.json

def test_get_posts_of_followed_users(authenticated_client):
    """Test fetching posts from followed users"""
    response = authenticated_client.get('/posts/followed')
    
    assert response.status_code == 200
    assert 'posts' in response.json

# Integration test for utility functions
def test_delete_vote_function():
    """Test the delete_vote utility function"""
    # Mock dependencies
    mock_session = Mock()
    mock_post = Mock()
    mock_vote = Mock()
    
    # Setup mock behavior
    mock_post_query = mock_session.query.return_value.get.return_value = mock_post
    mock_vote_query = (mock_session.query.return_value
                       .filter.return_value
                       .first.return_value) = mock_vote
    
    from your_app.posts import delete_vote
    
    # Call the function
    success, message, status_code = delete_vote(
        post_id=1,
        user_id=1,
        session=mock_session,
        Post=mock_post,
        Vote=mock_vote
    )
    
    # Assertions
    assert success is True
    assert status_code == 200
    assert message == "Vote deleted successfully"
    mock_session.delete.assert_called_once_with(mock_vote)
    mock_session.commit.assert_called_once()

def test_get_post_votes_function():
    """Test the get_post_votes utility function"""
    # Mock dependencies
    mock_session = Mock()
    mock_post = Mock()
    mock_vote = Mock()
    
    # Setup mock vote counting
    mock_session.query.return_value.filter.return_value.count.side_effect = [5, 3]
    
    from your_app.posts import get_post_votes
    
    # Call the function
    vote_counts = get_post_votes(
        post_id=1,
        session=mock_session,
        Post=mock_post,
        Vote=mock_vote
    )
    
    # Assertions
    assert vote_counts == {
        'upvotes': 5,
        'downvotes': 3,
        'total': 2
    }