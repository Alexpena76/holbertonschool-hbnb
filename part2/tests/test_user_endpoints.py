"""
Unit tests for User endpoints
"""

import unittest
import sys
import os

# Add the parent directory to the path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
import json


class TestUserEndpoints(unittest.TestCase):
    """Test cases for User API endpoints"""
    
    def setUp(self):
        """Set up test client before each test"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    def test_create_user_success(self):
        """Test successful user creation"""
        response = self.client.post('/api/v1/users', 
            json={
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "jane.doe.test@example.com"
            },
            content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], 'Jane')
        self.assertEqual(data['email'], 'jane.doe.test@example.com')
        print(f"✓ Created user: {data['id']}")

    def test_create_user_empty_first_name(self):
        """Test user creation with empty first name"""
        response = self.client.post('/api/v1/users',
            json={
                "first_name": "",
                "last_name": "Doe",
                "email": "empty.test@example.com"
            },
            content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        print(f"✓ Empty first name rejected: {data['error']}")

    def test_create_user_invalid_email(self):
        """Test user creation with invalid email"""
        response = self.client.post('/api/v1/users',
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": "invalid-email"
            },
            content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        print(f"✓ Invalid email rejected: {data['error']}")

    def test_create_user_missing_field(self):
        """Test user creation with missing required field"""
        response = self.client.post('/api/v1/users',
            json={
                "first_name": "John",
                "last_name": "Doe"
                # email is missing
            },
            content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        print("✓ Missing field rejected")

    def test_create_user_whitespace_name(self):
        """Test user creation with whitespace-only name"""
        response = self.client.post('/api/v1/users',
            json={
                "first_name": "   ",
                "last_name": "Doe",
                "email": "whitespace.test@example.com"
            },
            content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        print("✓ Whitespace name rejected")

    def test_get_user_success(self):
        """Test retrieving an existing user"""
        # Create user first
        create_response = self.client.post('/api/v1/users',
            json={
                "first_name": "GetTest",
                "last_name": "User",
                "email": "get.test.user@example.com"
            },
            content_type='application/json')
        
        user_id = json.loads(create_response.data)['id']
        
        # Get the user
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], user_id)
        print(f"✓ Retrieved user: {user_id}")

    def test_get_user_not_found(self):
        """Test retrieving a non-existent user"""
        response = self.client.get('/api/v1/users/nonexistent-id-12345')
        self.assertEqual(response.status_code, 404)
        print("✓ Non-existent user returns 404")

    def test_get_all_users(self):
        """Test retrieving all users"""
        # Create a user first
        self.client.post('/api/v1/users',
            json={
                "first_name": "ListTest",
                "last_name": "User",
                "email": "list.test.user@example.com"
            },
            content_type='application/json')
        
        response = self.client.get('/api/v1/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        print(f"✓ Retrieved {len(data)} users")

    def test_update_user_success(self):
        """Test successful user update"""
        # Create user first
        create_response = self.client.post('/api/v1/users',
            json={
                "first_name": "Original",
                "last_name": "Name",
                "email": "original.update@example.com"
            },
            content_type='application/json')
        
        user_id = json.loads(create_response.data)['id']
        
        # Update the user
        response = self.client.put(f'/api/v1/users/{user_id}',
            json={
                "first_name": "Updated",
                "last_name": "Name",
                "email": "updated.name@example.com"
            },
            content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        print(f"✓ Updated user: {user_id}")


if __name__ == '__main__':
    unittest.main(verbosity=2)