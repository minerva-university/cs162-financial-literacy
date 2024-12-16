import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from backend import create_app
from backend.database.create import Base, User, Scholarship, Internship, Post, Comment, Follow, MentorshipSession
from backend.auth import session as auth_session
from datetime import datetime
from dotenv import load_dotenv
import os

TEST_DB_URI =  os.getenv('TEST_DB_URI', 'sqlite:///test.db')

@pytest.fixture(scope='session')
def app():
    """
    Enhanced test application configuration
    """
    app = create_app({
        'TESTING': True,
        'SECRET_KEY': 'test_secret_key',
        'SQLALCHEMY_DATABASE_URI': TEST_DB_URI,
        'JWT_SECRET_KEY': 'test_jwt_secret',
        'MAIL_SUPPRESS_SEND': True,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'ERROR_404_HELP': False,
    })
    return app

@pytest.fixture(scope='session')
def test_engine():
    engine = create_engine(TEST_DB_URI)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope='function')
def db_session(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()
    session_factory = sessionmaker(bind=connection)
    Session = scoped_session(session_factory)
    session = Session()
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope='function')
def client(app, db_session):
    """
    Provides a test client for the Flask app
    """
    with app.test_client() as client:
        with app.app_context():
            auth_session.remove()
            auth_session.configure(bind=db_session.bind)
        yield client

@pytest.fixture(scope='function')
def create_user(db_session):
    """
    Enhanced user creation fixture supporting additional attributes
    """
    def _create(username, email, password, credits=100, **kwargs):
        user = User(
            username=username,
            email=email,
            credits=credits,
            **kwargs
        )
        user.set_password(password)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)  # Ensure we have the latest data
        return user
    return _create

@pytest.fixture
def login_user(client):
    def _login(email, password):
        return client.post('/login', json={"email": email, "password": password})
    return _login

@pytest.fixture(autouse=True)
def cleanup(db_session):
    """Cleanup all test data"""
    yield
    try:
        tables = [Post, Comment, User, Follow, MentorshipSession]  # Add all your models
        for table in tables:
            db_session.query(table).delete()
        db_session.commit()
    except Exception as e:
        print(f"Cleanup error: {e}")
        db_session.rollback()

@pytest.fixture(scope='function')
def app_context(app):
    """
    Ensures application context is available for tests
    """
    with app.app_context():
        yield

@pytest.fixture
def auth_headers(client, create_user, login_user):
    """
    Fixture to get authentication headers for API requests
    """
    def _get_headers(username="testuser", email="test@example.com", password="password123"):
        user = create_user(username=username, email=email, password=password)
        response = login_user(email=email, password=password)  # Fixed: was using wrong parameter
        token = response.json.get('access_token')
        if not token:
            raise ValueError("Login failed to return access token")
        return {'Authorization': f'Bearer {token}'}
    return _get_headers

@pytest.fixture
def mock_datetime(monkeypatch):
    """Fixture to mock datetime for consistent timestamps in tests"""
    class MockDateTime:
        @staticmethod
        def utcnow():
            return datetime(2024, 1, 1, 12, 0, 0)
    monkeypatch.setattr('backend.database.create.datetime', MockDateTime)
    return MockDateTime

@pytest.fixture
def test_data(db_session):
    """Fixture to populate database with test data"""
    def _create_test_data():
        # Add your common test data here
        user = User(username="testuser", email="testuser@example.com", credits=150)
        db_session.add(user)
        db_session.commit()
    return _create_test_data
