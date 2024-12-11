import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from backend import create_app
from backend.database.create import Base, User
from backend.auth import session as auth_session

TEST_DB_URI = "sqlite:///:memory:"

@pytest.fixture(scope='session')
def app():
    app = create_app({
        'TESTING': True,
        'SECRET_KEY': 'test_secret_key',
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
    Session = sessionmaker(bind=connection)
    session = scoped_session(Session)

    auth_session.remove()
    auth_session.configure(bind=connection)

    yield session

    session.remove()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope='function')
def client(app, db_session):
    with app.test_client() as client:
        yield client

@pytest.fixture
def create_user(db_session):
    def _create(username, email, password, credits=100):
        user = User(username=username, email=email, credits=credits)
        user.set_password(password)
        db_session.add(user)
        db_session.commit()
        return user
    return _create

@pytest.fixture
def login_user(client):
    def _login(email, password):
        return client.post('/login', json={"email": email, "password": password})
    return _login
