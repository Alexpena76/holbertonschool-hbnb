"""
Test User API Endpoints
"""

import unittest
import json
from app import create_app, db
from flask_jwt_extended import create_access_token


class TestUserEndpoints(unittest.TestCase):
    """Test cases for user endpoints"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = create_app('config.TestingConfig')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create admin token for protected routes
        self.admin_token = create_access_token(
            identity='admin-test-id',
            additional_claims={'is_admin': True}
        )
        self.admin_headers = {
            'Authorization': f'Bearer {self.admin_token}',
            'Content-Type': 'application/json'
        }
    
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_create_user_success(self):
        """Test successful user creation"""
        response = self.client.post('/api/v1/users',
            headers=self.admin_headers,
            json={
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "jane.doe.test@example.com",
                "password": "password123"
            })
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], 'Jane')
        self.assertEqual(data['last_name'], 'Doe')
        self.assertNotIn('password', data)
    
    def test_create_user_missing_field(self):
        """Test user creation with missing required field"""
        response = self.client.post('/api/v1/users',
            headers=self.admin_headers,
            json={
                "first_name": "John",
                "last_name": "Doe"
            })
        
        self.assertEqual(response.status_code, 400)
    
    def test_create_user_empty_first_name(self):
        """Test user creation with empty first name"""
        response = self.client.post('/api/v1/users',
            headers=self.admin_headers,
            json={
                "first_name": "",
                "last_name": "Doe",
                "email": "empty.test@example.com",
                "password": "password123"
            })
        
        self.assertEqual(response.status_code, 400)
    
    def test_create_user_invalid_email(self):
        """Test user creation with invalid email"""
        response = self.client.post('/api/v1/users',
            headers=self.admin_headers,
            json={
                "first_name": "John",
                "last_name": "Doe",
                "email": "invalid-email",
                "password": "password123"
            })
        
        self.assertEqual(response.status_code, 400)
    
    def test_create_user_whitespace_name(self):
        """Test user creation with whitespace-only name"""
        response = self.client.post('/api/v1/users',
            headers=self.admin_headers,
            json={
                "first_name": "   ",
                "last_name": "Doe",
                "email": "whitespace.test@example.com",
                "password": "password123"
            })
        
        self.assertEqual(response.status_code, 400)
    
    def test_create_user_without_admin(self):
        """Test that non-admin cannot create users"""
        # Create a regular user token
        regular_token = create_access_token(
            identity='regular-user-id',
            additional_claims={'is_admin': False}
        )
        regular_headers = {
            'Authorization': f'Bearer {regular_token}',
            'Content-Type': 'application/json'
        }
        
        response = self.client.post('/api/v1/users',
            headers=regular_headers,
            json={
                "first_name": "Test",
                "last_name": "User",
                "email": "test@example.com",
                "password": "password123"
            })
        
        self.assertEqual(response.status_code, 403)
    
    def test_get_all_users(self):
        """Test retrieving all users"""
        response = self.client.get('/api/v1/users')
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data), list)
    
    def test_get_user_not_found(self):
        """Test retrieving non-existent user"""
        response = self.client.get('/api/v1/users/nonexistent-id')
        
        self.assertEqual(response.status_code, 404)
    
    def test_get_user_success(self):
        """Test retrieving an existing user"""
        # Create user first
        create_response = self.client.post('/api/v1/users',
            headers=self.admin_headers,
            json={
                "first_name": "GetTest",
                "last_name": "User",
                "email": "get.test.user@example.com",
                "password": "password123"
            })
        
        self.assertEqual(create_response.status_code, 201)
        user_id = json.loads(create_response.data)['id']
        
        # Get the user
        response = self.client.get(f'/api/v1/users/{user_id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], 'GetTest')
    
    def test_update_user_success(self):
        """Test successful user update"""
        # Create user first
        create_response = self.client.post('/api/v1/users',
            headers=self.admin_headers,
            json={
                "first_name": "Original",
                "last_name": "Name",
                "email": "original.update@example.com",
                "password": "password123"
            })
        
        self.assertEqual(create_response.status_code, 201)
        user_id = json.loads(create_response.data)['id']
        
        # Update with admin token
        response = self.client.put(f'/api/v1/users/{user_id}',
            headers=self.admin_headers,
            json={
                "first_name": "Updated",
                "last_name": "Name",
                "email": "original.update@example.com",
                "password": "password123"
            })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['first_name'], 'Updated')


if __name__ == '__main__':
    unittest.main()