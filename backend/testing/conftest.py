import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from backend import create_app
from backend.database.create import Base, User, Scholarship, Internship, Post, Comment, Follow, MentorshipSession

TEST_DB_URI = 'sqlite:///:memory:'

@pytest.fixture(scope='session')
def app():
    """
    Create and configure a new app instance for tests.
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
    """
    Create a test database engine and setup the database schema.
    """
    engine = create_engine(TEST_DB_URI)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope='function')
def db_session(test_engine):
    """
    Provide a transactional scope around a series of operations.
    """
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
    Provides a test client for the Flask app.
    Sets app.session_factory to return the test db_session so that
    all database queries use this session.
    """
    with app.test_client() as client:
        with app.app_context():
            app.session_factory = lambda: db_session
        yield client

@pytest.fixture(scope='function')
def create_user(db_session):
    """
    Fixture to create a user in the test database.
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
        db_session.refresh(user)
        return user
    return _create

@pytest.fixture
def login_user(client):
    """
    Fixture to log a user in using the test client.
    """
    def _login(email, password):
        return client.post('/login', json={"email": email, "password": password})
    return _login

@pytest.fixture(autouse=True)
def cleanup(db_session):
    """
    Cleanup fixture to remove all test data after each test.
    Ensures a clean state for subsequent tests.
    """
    yield
    try:
        tables = [Post, Comment, User, Follow, MentorshipSession]
        for table in tables:
            db_session.query(table).delete()
        db_session.commit()
    except Exception as e:
        print(f"Cleanup error: {e}")
        db_session.rollback()

@pytest.fixture
def auth_headers(client, create_user, login_user):
    """
    Fixture to retrieve auth headers (like a JWT) for requests if needed.
    """
    def _get_headers(username="testuser", email="test@example.com", password="password123"):
        user = create_user(username=username, email=email, password=password)
        response = login_user(email=email, password=password)
        token = response.json.get('access_token')
        if not token:
            raise ValueError("Login failed to return access token")
        return {'Authorization': f'Bearer {token}'}
    return _get_headers
