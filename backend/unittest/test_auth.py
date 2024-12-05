import pytest
from flask import Flask, json
from werkzeug.security import generate_password_hash
from backend.auth import auth
from backend.database.create import User, engine
from sqlalchemy.orm import sessionmaker

TestSession = sessionmaker(bind=engine)

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    app.register_blueprint(auth)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_signup_success(client):
    """Test successful user registration"""
    response = client.post('/signup', json={
        'email': 'test@example.com',
        'name': 'Test User',
        'password': 'testpassword123'
    })
    
    assert response.status_code == 200, "Expected status code 200, got {}".format(response.status_code)
    assert json.loads(response.data)['success'] == 'Yes', "Expected success message, got {}".format(response.data)
    print("test_signup_success passed")

def test_signup_duplicate_email(client):
    """Test signup with existing email"""
    # First signup
    client.post('/signup', json={
        'email': 'test@example.com',
        'name': 'Test User',
        'password': 'testpassword123'
    })
    
    # Try to signup again with same email
    response = client.post('/signup', json={
        'email': 'test@example.com',
        'name': 'Another User',
        'password': 'password123'
    })
    
    assert response.status_code == 400, "Expected status code 400, got {}".format(response.status_code)
    assert 'User already exists' in json.loads(response.data)['reason'], "Expected 'User already exists' message, got {}".format(response.data)
    print("test_signup_duplicate_email passed")

def test_login_success(client):
    """Test successful login"""
    # Create user first
    client.post('/signup', json={
        'email': 'test@example.com',
        'name': 'Test User',
        'password': 'testpassword123'
    })
    
    # Try to login
    response = client.post('/login', json={
        'email': 'test@example.com',
        'password': 'testpassword123'
    })
    
    assert response.status_code == 200, "Expected status code 200, got {}".format(response.status_code)
    assert json.loads(response.data)['success'] == 'Yes', "Expected success message, got {}".format(response.data)
    print("test_login_success passed")

def test_login_invalid_credentials(client):
    """Test login with wrong password"""
    response = client.post('/login', json={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    })
    
    assert response.status_code == 200, "Expected status code 200, got {}".format(response.status_code)
    assert json.loads(response.data)['success'] == 'No', "Expected failure message, got {}".format(response.data)
    print("test_login_invalid_credentials passed")

def test_logout(client):
    """Test logout functionality"""
    # Login first
    client.post('/login', json={
        'email': 'test@example.com',
        'password': 'testpassword123'
    })
    
    # Then logout
    response = client.get('/logout')
    assert response.status_code == 200, "Expected status code 200, got {}".format(response.status_code)
    print("test_logout passed")

def test_ping_authenticated(client):
    """Test ping endpoint when authenticated"""
    # Login first
    client.post('/login', json={
        'email': 'test@example.com',
        'password': 'testpassword123'
    })
    
    response = client.get('/ping')
    data = json.loads(response.data)
    assert data['authenticated'] == True, "Expected authenticated to be True, got {}".format(data['authenticated'])
    assert 'username' in data, "Expected 'username' in response data, got {}".format(data)
    print("test_ping_authenticated passed")

def test_ping_unauthenticated(client):
    """Test ping endpoint when not authenticated"""
    response = client.get('/ping')
    data = json.loads(response.data)
    assert data['authenticated'] == False, "Expected authenticated to be False, got {}".format(data['authenticated'])
    print("test_ping_unauthenticated passed")

def test_login_missing_email(client):
    """Test login with missing email"""
    response = client.post('/login', json={
        'password': 'testpassword123'
    })
    assert response.status_code == 200, "Expected status code 200, got {}".format(response.status_code)
    assert json.loads(response.data)['success'] == 'No', "Expected failure message, got {}".format(response.data)
    print("test_login_missing_email passed")

def test_login_missing_password(client):
    """Test login with missing password"""
    response = client.post('/login', json={
        'email': 'test@example.com'
    })
    assert response.status_code == 200, "Expected status code 200, got {}".format(response.status_code)
    assert json.loads(response.data)['success'] == 'No', "Expected failure message, got {}".format(response.data)
    print("test_login_missing_password passed")

def test_signup_missing_email(client):
    """Test signup with missing email"""
    response = client.post('/signup', json={
        'name': 'Test User',
        'password': 'testpassword123'
    })
    assert response.status_code == 400, "Expected status code 400, got {}".format(response.status_code)
    assert 'Email is required' in json.loads(response.data)['reason'], "Expected 'Email is required' message, got {}".format(response.data)
    print("test_signup_missing_email passed")

def test_signup_missing_name(client):
    """Test signup with missing name"""
    response = client.post('/signup', json={
        'email': 'test@example.com',
        'password': 'testpassword123'
    })
    assert response.status_code == 400, "Expected status code 400, got {}".format(response.status_code)
    assert 'Name is required' in json.loads(response.data)['reason'], "Expected 'Name is required' message, got {}".format(response.data)
    print("test_signup_missing_name passed")

def test_signup_missing_password(client):
    """Test signup with missing password"""
    response = client.post('/signup', json={
        'email': 'test@example.com',
        'name': 'Test User'
    })
    assert response.status_code == 400, "Expected status code 400, got {}".format(response.status_code)
    assert 'Password is required' in json.loads(response.data)['reason'], "Expected 'Password is required' message, got {}".format(response.data)
    print("test_signup_missing_password passed")

def test_get_available_mentors(client):
    """Test get available mentors"""
    user = User(email='mentor@example.com', name='Mentor', mentorship_availability=True)
    session = TestSession()
    session.add(user)
    session.commit()
    response = client.get('/mentors/available')
    assert response.status_code == 200, "Expected status code 200, got {}".format(response.status_code)
    assert len(json.loads(response.data)['mentors']) > 0, "Expected at least one mentor, got {}".format(response.data)
    assert json.loads(response.data)['mentors'][0]['name'] == 'Mentor', "Expected mentor name 'Mentor', got {}".format(response.data)
    print("test_get_available_mentors passed")