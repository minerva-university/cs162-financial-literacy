import unittest
import json
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from flask import Flask
from flask_login import LoginManager, login_user, current_user

# Import the blueprint and necessary models
from backend.scholarships_internships import scholarships_internships
from backend.database.create import User, Scholarship, Internship, Organization
from backend.config import COST_TO_ACCESS, REWARD_FOR_POSTING

class ScholarshipsInternshipsTestCase(unittest.TestCase):
    def setUp(self):
        # Create a Flask test client
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = 'test_secret_key'
        
        # Register the blueprint
        self.app.register_blueprint(scholarships_internships)
        
        # Setup login manager
        login_manager = LoginManager()
        login_manager.init_app(self.app)
        
        # Create a test client
        self.client = self.app.test_client()
        
        # Mock database session and user
        self.session_patcher = patch('your_app.scholarships_internships.Session')
        self.mock_session_class = self.session_patcher.start()
        self.mock_session = MagicMock()
        self.mock_session_class.return_value = self.mock_session
        
        # Create a mock user
        self.mock_user = MagicMock(spec=User)
        self.mock_user.user_id = 1
        self.mock_user.credits = 100
        
        # Mock current_user
        self.current_user_patcher = patch('your_app.scholarships_internships.current_user', self.mock_user)
        self.current_user_patcher.start()
        
        # Login the mock user
        with self.app.test_request_context():
            login_user(self.mock_user)

    def tearDown(self):
        # Stop all patches
        self.session_patcher.stop()
        self.current_user_patcher.stop()

    def test_get_scholarships_success(self):
        """Test retrieving scholarships successfully"""
        # Mock the query to return some scholarships
        mock_scholarship = MagicMock(spec=Scholarship)
        mock_scholarship.scholarship_id = 1
        mock_scholarship.title = "Test Scholarship"
        mock_scholarship.description = "Test Description"
        mock_scholarship.organization = MagicMock(name="Test Org")
        
        self.mock_session.query.return_value.filter_by.return_value.first.return_value = self.mock_user
        self.mock_session.query.return_value.all.return_value = [mock_scholarship]
        
        # Make the request
        response = self.client.get('/scholarships')
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('scholarships', data)
        self.assertEqual(len(data['scholarships']), 1)
        self.assertEqual(data['scholarships'][0]['title'], "Test Scholarship")

    def test_post_scholarship_success(self):
        """Test posting a new scholarship"""
        # Prepare scholarship data
        scholarship_data = {
            'title': 'New Scholarship',
            'description': 'Scholarship description',
            'eligibility': 'Open to all',
            'application_link': 'http://example.com'
        }
        
        # Mock the session queries
        self.mock_session.query.return_value.filter_by.return_value.first.return_value = self.mock_user
        
        # Make the request
        response = self.client.post('/scholarships', 
                                    data=json.dumps(scholarship_data), 
                                    content_type='application/json')
        
        # Check the response
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('success', data)
        self.assertIn('scholarship_id', data)
        self.assertIn('credits', data)

    def test_get_scholarship_insufficient_credits(self):
        """Test retrieving scholarships with insufficient credits"""
        # Mock user with zero credits
        self.mock_user.credits = 0
        
        # Make the request
        response = self.client.get('/scholarships')
        
        # Check the response
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Insufficient credits')

    def test_filter_scholarships(self):
        """Test filtering scholarships"""
        # Mock scholarship query
        mock_scholarship = MagicMock(spec=Scholarship)
        mock_scholarship.scholarship_id = 1
        mock_scholarship.title = "Engineering Scholarship"
        mock_scholarship.amount = 5000
        mock_scholarship.organization = MagicMock(name="Tech Org")
        
        self.mock_session.query.return_value.filter_by.return_value.first.return_value = self.mock_user
        self.mock_session.query.return_value.filter.return_value.join.return_value.filter.return_value.all.return_value = [mock_scholarship]
        
        # Make the request with filters
        response = self.client.get('/scholarships/filter?title=Engineering&min_amount=1000')
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('scholarships', data)
        self.assertEqual(len(data['scholarships']), 1)
        self.assertEqual(data['scholarships'][0]['title'], "Engineering Scholarship")

    def test_update_scholarship(self):
        """Test updating an existing scholarship"""
        # Mock the scholarship query
        mock_scholarship = MagicMock(spec=Scholarship)
        mock_scholarship.scholarship_id = 1
        mock_scholarship.title = "Original Title"
        mock_scholarship.user_id = self.mock_user.user_id
        
        self.mock_session.query.return_value.filter_by.return_value.first.return_value = mock_scholarship
        
        # Prepare update data
        update_data = {
            'title': 'Updated Scholarship Title'
        }
        
        # Make the request
        response = self.client.put('/scholarships/1', 
                                   data=json.dumps(update_data), 
                                   content_type='application/json')
        
        # Check the response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('success', data)

    def test_internships_similar_scenarios(self):
        """Test similar scenarios for internships"""
        # Create similar test methods for internships routes
        # (Similar to scholarship tests but with internship-specific data)
        pass

    def test_delete_listing(self):
        """Test deleting a scholarship or internship"""
        # Mock a successful deletion
        mock_listing = MagicMock()
        mock_listing.user_id = self.mock_user.user_id
        
        self.mock_session.query.return_value.get.return_value = mock_listing
        
        # Test scholarship deletion
        response = self.client.delete('/api/scholarship/1')
        self.assertEqual(response.status_code, 200)
        
        # Test internship deletion
        response = self.client.delete('/api/internship/1')
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_delete(self):
        """Test deletion attempt by unauthorized user"""
        # Mock a listing with a different user ID
        mock_listing = MagicMock()
        mock_listing.user_id = 999  # Different from current user
        
        self.mock_session.query.return_value.get.return_value = mock_listing
        
        # Test scholarship deletion
        response = self.client.delete('/api/scholarship/1')
        self.assertEqual(response.status_code, 400)

    def test_search_scholarships(self):
        """Test searching and ordering scholarships"""
        # Mock scholarship query with search and ordering
        mock_scholarship = MagicMock(spec=Scholarship)
        mock_scholarship.scholarship_id = 1
        mock_scholarship.title = "Research Scholarship"
        mock_scholarship.deadline = datetime.now(timezone.utc)
        mock_scholarship.status = MagicMock(value='ACTIVE')
        
        self.mock_session.query.return_value.filter_by.return_value.first.return_value = self.mock_user
        self.mock_session.query.return_value.filter.return_value.join.return_value.filter.return_value.order_by.return_value.all.return_value = [mock_scholarship]
        
        # Test search with deadline ordering
        response = self.client.get('/scholarships/search?order_by=deadline')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('scholarships', data)

        # Test search with newest ordering
        response = self.client.get('/scholarships/search?order_by=newest')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('scholarships', data)

if __name__ == '__main__':
    unittest.main()