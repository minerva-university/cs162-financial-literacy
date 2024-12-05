import pytest
from flask import Flask
from flask_login import LoginManager, current_user
from unittest.mock import Mock
from backend.database.create import User, engine
from sqlalchemy.orm import sessionmaker

TestSession = sessionmaker(bind=engine)

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    
    # Initialize LoginManager
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
    return app.test_client()

@pytest.fixture
def mock_user():
    user = Mock(spec=User)
    user.user_id = 1
    user.name = 'Test User'
    user.email = 'test@example.com'
    user.credits = 100
    user.is_authenticated = True
    return user

@pytest.fixture
def auth_client(client, app, mock_user):
    with app.test_request_context():
        login_user(mock_user)
    return client

#Will print all tests passed when all tests pass
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    if exitstatus == 0:
        terminalreporter.write_sep("=", "All tests passed!")