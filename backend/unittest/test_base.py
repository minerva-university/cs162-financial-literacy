# backend/unittest/test_base.py
import os
import unittest
from flask import Flask
from flask_login import LoginManager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from backend import create_app  # Assuming you have a factory function to create the Flask app
from backend.database.create import Base, User, engine as main_engine


class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use a test database URI if provided, else default to in-memory SQLite
        test_db_uri = os.environ.get('TEST_DB_URI', 'sqlite:///:memory:')
        cls.test_engine = create_engine(test_db_uri)
        Base.metadata.create_all(bind=cls.test_engine)
        cls.Session = sessionmaker(bind=cls.test_engine)
        
        # Create the Flask test app
        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.app.config['LOGIN_DISABLED'] = False
        cls.client = cls.app.test_client()
        
    def setUp(self):
        # Each test runs in a transaction that we roll back at the end
        self.connection = self.test_engine.connect()
        self.transaction = self.connection.begin()
        self.session = self.Session(bind=self.connection)
        
        # Patch the app's sessionmaker if necessary, or ensure your endpoints use a session factory
        # If your code directly uses Session = sessionmaker(bind=engine), consider refactoring to allow test injection
        # For demonstration, we assume endpoints can be tested as is if they rely on engine from the environment.
        
        # If needed, monkeypatch the session within the tests:
        # Example (if your endpoints rely on `session` global):
        # from backend.auth import session as auth_session
        # auth_session.bind = self.connection
        
    def tearDown(self):
        self.session.close()
        self.transaction.rollback()
        self.connection.close()
    
    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=cls.test_engine)
    
    def register_user(self, email, password, name="Test User"):
        return self.client.post('/signup', json={
            "email": email,
            "password": password,
            "name": name
        })

    def login_user(self, email, password):
        return self.client.post('/login', json={
            "email": email,
            "password": password
        })

    def logout_user(self):
        return self.client.get('/logout')
