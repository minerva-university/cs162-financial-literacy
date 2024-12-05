import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

import unittest
import json
from flask import Flask
from flask_login import LoginManager, login_user, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from backend.mentorship import mentorship_bp
from backend.database.create import User, MentorshipSession, engine
from sqlalchemy.orm import sessionmaker
from backend.config import COST_TO_BOOK_MENTORSHIP, REWARD_FOR_MENTORING


class MentorshipBlueprintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a test Flask app
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.config['SECRET_KEY'] = 'test_secret_key'
        cls.app.register_blueprint(mentorship_bp)

        # Setup login manager
        cls.login_manager = LoginManager()
        cls.login_manager.init_app(cls.app)

        # Create test session
        cls.Session = sessionmaker(bind=engine)

        # Setup user loader
        @cls.login_manager.user_loader
        def load_user(user_id):
            session = cls.Session()
            return session.query(User).get(int(user_id))

    def setUp(self):
        # Create a test client
        self.client = self.app.test_client()

        # Prepare test database
        session = self.Session()

        # Create test users
        self.mentee = User(
            name='Test Mentee', 
            email='mentee@example.com', 
            password=generate_password_hash('password123'),
            credits=100,
            is_mentor=False
        )
        self.mentor = User(
            name='Test Mentor', 
            email='mentor@example.com', 
            password=generate_password_hash('password456'),
            credits=50,
            is_mentor=True,
            bio='Experienced professional'
        )

        session.add(self.mentee)
        session.add(self.mentor)
        session.commit()

        # Login as mentee
        with self.app.test_request_context():
            login_user(self.mentee)

        self.session = session

    def tearDown(self):
        # Clean up database after each test
        session = self.Session()
        session.query(MentorshipSession).delete()
        session.query(User).delete()
        session.commit()
        session.close()

    def login_as_mentee(self):
        with self.app.test_request_context():
            login_user(self.mentee)

    def login_as_mentor(self):
        with self.app.test_request_context():
            login_user(self.mentor)

    def test_book_mentorship_success(self):
        """Test successfully booking a mentorship session"""
        # Login as mentee
        self.login_as_mentee()

        # Prepare booking data
        booking_data = {
            'mentor_id': self.mentor.user_id,
            'scheduled_time': datetime.now() + timedelta(days=7)
        }

        # Send booking request
        response = self.client.post(
            '/mentorship/book', 
            data=json.dumps(booking_data),
            content_type='application/json'
        )

        # Verify response
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertIn('session_id', response_data)
        
        # Verify credits deducted
        updated_mentee = self.session.query(User).get(self.mentee.user_id)
        self.assertEqual(updated_mentee.credits, 100 - COST_TO_BOOK_MENTORSHIP)

    def test_book_mentorship_insufficient_credits(self):
        """Test booking mentorship with insufficient credits"""
        # Create a user with zero credits
        broke_user = User(
            name='Broke User', 
            email='broke@example.com', 
            password=generate_password_hash('password789'),
            credits=0,
            is_mentor=False
        )
        self.session.add(broke_user)
        self.session.commit()

        # Login as broke user
        with self.app.test_request_context():
            login_user(broke_user)

        # Prepare booking data
        booking_data = {
            'mentor_id': self.mentor.user_id,
            'scheduled_time': datetime.now() + timedelta(days=7)
        }

        # Send booking request
        response = self.client.post(
            '/mentorship/book', 
            data=json.dumps(booking_data),
            content_type='application/json'
        )

        # Verify response
        self.assertEqual(response.status_code, 403)
        response_data = json.loads(response.data)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Insufficient credits')

    def test_complete_mentorship_success(self):
        """Test successfully completing a mentorship session"""
        # Create a scheduled session
        session = self.Session()
        mentorship_session = MentorshipSession(
            mentee_id=self.mentee.user_id,
            mentor_id=self.mentor.user_id,
            scheduled_time=datetime.now() - timedelta(days=1),
            status='scheduled'
        )
        session.add(mentorship_session)
        session.commit()

        # Login as mentor
        self.login_as_mentor()

        # Send complete request
        response = self.client.post(f'/mentorship/complete/{mentorship_session.session_id}')

        # Verify response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('message', response_data)
        
        # Verify mentor credits added
        updated_mentor = self.session.query(User).get(self.mentor.user_id)
        self.assertEqual(updated_mentor.credits, 50 + REWARD_FOR_MENTORORING)

        # Verify session status updated
        updated_session = self.session.query(MentorshipSession).get(mentorship_session.session_id)
        self.assertEqual(updated_session.status, 'completed')

    def test_cancel_mentorship_by_mentee(self):
        """Test canceling a mentorship session by mentee"""
        # Create a scheduled session
        session = self.Session()
        mentorship_session = MentorshipSession(
            mentee_id=self.mentee.user_id,
            mentor_id=self.mentor.user_id,
            scheduled_time=datetime.now() + timedelta(days=7),
            status='scheduled'
        )
        session.add(mentorship_session)
        session.commit()

        # Login as mentee
        self.login_as_mentee()

        # Send cancel request
        response = self.client.post(f'/mentorship/cancel/{mentorship_session.session_id}')

        # Verify response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('message', response_data)
        
        # Verify mentee credits refunded
        updated_mentee = self.session.query(User).get(self.mentee.user_id)
        self.assertEqual(updated_mentee.credits, 100)  # Credits should be back to original amount

        # Verify session status updated
        updated_session = self.session.query(MentorshipSession).get(mentorship_session.session_id)
        self.assertEqual(updated_session.status, 'canceled')

    def test_get_available_mentors(self):
        """Test retrieving available mentors"""
        # Login as mentee
        self.login_as_mentee()

        # Send get mentors request
        response = self.client.get('/mentors')

        # Verify response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('mentors', response_data)
        
        # Verify mentor details
        mentors = response_data['mentors']
        self.assertTrue(len(mentors) > 0)
        mentor_details = mentors[0]
        self.assertIn('id', mentor_details)
        self.assertIn('name', mentor_details)
        self.assertIn('bio', mentor_details)

    def test_get_user_credits(self):
        """Test retrieving user credits"""
        # Login as mentee
        self.login_as_mentee()

        # Send get credits request
        response = self.client.get('/mentorship/get_credits')

        # Verify response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('credits', response_data)
        self.assertEqual(response_data['credits'], 100)

if __name__ == '__main__':
    unittest.main()