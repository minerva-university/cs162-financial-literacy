import pytest
from flask import json
from flask_login import login_user, current_user

# Import the profile blueprint from the backend.
from backend.profile import profile

# Import the database models and engine.
from backend.database.create import User, Follow, engine

# Import the SQLAlchemy sessionmaker.
from sqlalchemy.orm import sessionmaker

# Create a test session factory
TestSession = sessionmaker(bind=engine)

@pytest.fixture
def app():
    """Create a Flask app with the profile blueprint"""
    from flask import Flask
    from flask_login import LoginManager
    
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    
    # Register the blueprint
    app.register_blueprint(profile)
    
    # Setup Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        session = TestSession()
        user = session.query(User).get(int(user_id))
        session.close()
        return user
    
    return app

@pytest.fixture
def client(app):
    """Create a test client for making requests"""
    return app.test_client()

@pytest.fixture
def logged_in_user(app):
    """Create and log in a test user"""
    session = TestSession()
    
    # Create a test user
    test_user = User(
        email='testuser@example.com', 
        name='Test User', 
        bio='Test Bio', 
        password='testpassword'  # Ensure proper password hashing in actual implementation
    )
    session.add(test_user)
    session.commit()
    
    # Create another user to follow
    target_user = User(
        email='targetuser@example.com', 
        name='Target User', 
        bio='Target Bio',
        password='targetpassword'
    )
    session.add(target_user)
    session.commit()
    
    # Simulate login
    with app.test_request_context():
        login_user(test_user)
    
    yield test_user, target_user
    
    # Cleanup
    session = TestSession()
    session.query(User).filter(User.email.in_(['testuser@example.com', 'targetuser@example.com'])).delete()
    session.query(Follow).filter(
        (Follow.follower_id == test_user.user_id) | 
        (Follow.followed_id == test_user.user_id) |
        (Follow.follower_id == target_user.user_id) | 
        (Follow.followed_id == target_user.user_id)
    ).delete()
    session.commit()
    session.close()

def test_update_profile_success(client, logged_in_user):
    """Test successful profile update"""
    test_user, _ = logged_in_user
    
    # Update profile
    response = client.post('/profile', json={
        'name': 'Updated Name',
        'bio': 'Updated Bio'
    })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['updated_profile']['name'] == 'Updated Name'
    assert data['updated_profile']['bio'] == 'Updated Bio'

def test_update_profile_invalid_data(client, logged_in_user):
    """Test profile update with invalid data"""
    response = client.post('/profile', data='invalid json')
    
    assert response.status_code == 400

def test_get_followings_empty(client, logged_in_user):
    """Test retrieving followings when no users are followed"""
    response = client.get('/profile')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert 'followings' in data
    assert len(data['followings']) == 0

def test_get_followings_with_follow(client, logged_in_user):
    """Test retrieving followings after following a user"""
    test_user, target_user = logged_in_user
    
    # Create a follow relationship
    session = TestSession()
    follow = Follow(follower_id=test_user.user_id, followed_id=target_user.user_id)
    session.add(follow)
    session.commit()
    
    # Get followings
    response = client.get('/profile')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert target_user.name in data['followings']
    
    # Cleanup
    session.delete(follow)
    session.commit()
    session.close()

def test_follow_user_success(client, logged_in_user):
    """Test successfully following a user"""
    _, target_user = logged_in_user
    
    # Follow user
    response = client.post('/follow', json={
        'user_id': target_user.user_id
    })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['success'] == 'Successfully followed user'
    assert data['following']['user_id'] == target_user.user_id

def test_follow_user_self(client, logged_in_user):
    """Test attempting to follow self"""
    test_user, _ = logged_in_user
    
    # Try to follow self
    response = client.post('/follow', json={
        'user_id': test_user.user_id
    })
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Cannot follow yourself' in data['error']

def test_follow_user_already_following(client, logged_in_user):
    """Test attempting to follow a user already being followed"""
    _, target_user = logged_in_user
    
    # First follow
    client.post('/follow', json={
        'user_id': target_user.user_id
    })
    
    # Try to follow again
    response = client.post('/follow', json={
        'user_id': target_user.user_id
    })
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Already following this user' in data['error']

def test_unfollow_user_success(client, logged_in_user):
    """Test successfully unfollowing a user"""
    test_user, target_user = logged_in_user
    
    # First follow the user
    client.post('/follow', json={
        'user_id': target_user.user_id
    })
    
    # Now unfollow
    response = client.post('/unfollow', json={
        'user_id': target_user.user_id
    })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    
    assert data['success'] == 'Successfully unfollowed user'
    assert data['unfollowed']['user_id'] == target_user.user_id

def test_unfollow_user_not_following(client, logged_in_user):
    """Test attempting to unfollow a user not being followed"""
    _, target_user = logged_in_user
    
    # Try to unfollow without following first
    response = client.post('/unfollow', json={
        'user_id': target_user.user_id
    })
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Not following this user' in data['error']

def test_unfollow_nonexistent_user(client, logged_in_user):
    """Test attempting to unfollow a nonexistent user"""
    response = client.post('/unfollow', json={
        'user_id': 99999  # Assuming this ID doesn't exist
    })
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'Target user not found' in data['error']