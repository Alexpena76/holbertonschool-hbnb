"""
Test Amenity API Endpoints
"""

import unittest
import json
from app import create_app, db
from flask_jwt_extended import create_access_token


class TestAmenityEndpoints(unittest.TestCase):
    """Test cases for amenity endpoints"""
    
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
    
    def test_create_amenity_success(self):
        """Test successful amenity creation"""
        response = self.client.post('/api/v1/amenities',
            headers=self.admin_headers,
            json={"name": "WiFi Test"})
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'WiFi Test')
    
    def test_create_amenity_empty_name(self):
        """Test amenity creation with empty name"""
        response = self.client.post('/api/v1/amenities',
            headers=self.admin_headers,
            json={"name": ""})
        
        self.assertEqual(response.status_code, 400)
    
    def test_create_amenity_whitespace_name(self):
        """Test amenity creation with whitespace-only name"""
        response = self.client.post('/api/v1/amenities',
            headers=self.admin_headers,
            json={"name": "   "})
        
        self.assertEqual(response.status_code, 400)
    
    def test_create_amenity_duplicate_name(self):
        """Test amenity creation with duplicate name"""
        # Create first amenity
        self.client.post('/api/v1/amenities',
            headers=self.admin_headers,
            json={"name": "Duplicate Test"})
        
        # Try to create duplicate
        response = self.client.post('/api/v1/amenities',
            headers=self.admin_headers,
            json={"name": "Duplicate Test"})
        
        self.assertEqual(response.status_code, 400)
    
    def test_create_amenity_without_admin(self):
        """Test that non-admin cannot create amenities"""
        regular_token = create_access_token(
            identity='regular-user-id',
            additional_claims={'is_admin': False}
        )
        regular_headers = {
            'Authorization': f'Bearer {regular_token}',
            'Content-Type': 'application/json'
        }
        
        response = self.client.post('/api/v1/amenities',
            headers=regular_headers,
            json={"name": "Test Amenity"})
        
        self.assertEqual(response.status_code, 403)
    
    def test_get_all_amenities(self):
        """Test retrieving all amenities"""
        response = self.client.get('/api/v1/amenities')
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data), list)
    
    def test_get_amenity_not_found(self):
        """Test retrieving non-existent amenity"""
        response = self.client.get('/api/v1/amenities/nonexistent-id')
        
        self.assertEqual(response.status_code, 404)
    
    def test_get_amenity_success(self):
        """Test retrieving an existing amenity"""
        # Create amenity first
        create_response = self.client.post('/api/v1/amenities',
            headers=self.admin_headers,
            json={"name": "Pool Test"})
        
        self.assertEqual(create_response.status_code, 201)
        amenity_id = json.loads(create_response.data)['id']
        
        # Get the amenity
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Pool Test')
    
    def test_update_amenity_success(self):
        """Test successful amenity update"""
        # Create amenity first
        create_response = self.client.post('/api/v1/amenities',
            headers=self.admin_headers,
            json={"name": "Original Amenity"})
        
        self.assertEqual(create_response.status_code, 201)
        amenity_id = json.loads(create_response.data)['id']
        
        # Update the amenity
        response = self.client.put(f'/api/v1/amenities/{amenity_id}',
            headers=self.admin_headers,
            json={"name": "Updated Amenity"})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Updated Amenity')


if __name__ == '__main__':
    unittest.main()