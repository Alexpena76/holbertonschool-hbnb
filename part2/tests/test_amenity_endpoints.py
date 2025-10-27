"""
Unit tests for Amenity endpoints
"""

import unittest
import sys
import os

# Add the parent directory to the path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
import json


class TestAmenityEndpoints(unittest.TestCase):
    """Test cases for Amenity API endpoints"""
    
    def setUp(self):
        """Set up test client before each test"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    def test_create_amenity_success(self):
        """Test successful amenity creation"""
        response = self.client.post('/api/v1/amenities',
            json={"name": "WiFi Test"},
            content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'WiFi Test')
        print(f"✓ Created amenity: {data['id']}")

    def test_create_amenity_empty_name(self):
        """Test amenity creation with empty name"""
        response = self.client.post('/api/v1/amenities',
            json={"name": ""},
            content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        print("✓ Empty amenity name rejected")

    def test_create_amenity_whitespace_name(self):
        """Test amenity creation with whitespace-only name"""
        response = self.client.post('/api/v1/amenities',
            json={"name": "   "},
            content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        print("✓ Whitespace amenity name rejected")

    def test_create_amenity_duplicate_name(self):
        """Test amenity creation with duplicate name"""
        # Create first amenity
        self.client.post('/api/v1/amenities',
            json={"name": "Duplicate Test"},
            content_type='application/json')
        
        # Try to create duplicate
        response = self.client.post('/api/v1/amenities',
            json={"name": "Duplicate Test"},
            content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        print("✓ Duplicate amenity name rejected")

    def test_get_amenity_success(self):
        """Test retrieving an existing amenity"""
        # Create amenity first
        create_response = self.client.post('/api/v1/amenities',
            json={"name": "Pool Test"},
            content_type='application/json')
        
        amenity_id = json.loads(create_response.data)['id']
        
        # Get the amenity
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], amenity_id)
        print(f"✓ Retrieved amenity: {amenity_id}")

    def test_get_amenity_not_found(self):
        """Test retrieving a non-existent amenity"""
        response = self.client.get('/api/v1/amenities/nonexistent-id-12345')
        self.assertEqual(response.status_code, 404)
        print("✓ Non-existent amenity returns error")

    def test_get_all_amenities(self):
        """Test retrieving all amenities"""
        # Create an amenity first
        self.client.post('/api/v1/amenities',
            json={"name": "Parking Test"},
            content_type='application/json')
        
        response = self.client.get('/api/v1/amenities')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        print(f"✓ Retrieved {len(data)} amenities")

    def test_update_amenity_success(self):
        """Test successful amenity update"""
        # Create amenity first
        create_response = self.client.post('/api/v1/amenities',
            json={"name": "Original Amenity"},
            content_type='application/json')
        
        amenity_id = json.loads(create_response.data)['id']
        
        # Update the amenity
        response = self.client.put(f'/api/v1/amenities/{amenity_id}',
            json={"name": "Updated Amenity"},
            content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        print(f"✓ Updated amenity: {amenity_id}")


if __name__ == '__main__':
    unittest.main(verbosity=2)
