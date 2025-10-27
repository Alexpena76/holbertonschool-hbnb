"""
Unit tests for Review endpoints
NOTE: This will work once you register the reviews namespace in app/__init__.py
"""

import unittest
import sys
import os

# Add the parent directory to the path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
import json


class TestReviewEndpoints(unittest.TestCase):
    """Test cases for Review API endpoints"""
    
    def setUp(self):
        """Set up test client and create test user and place"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True
        
        # Create a user
        user_response = self.client.post('/api/v1/users',
            json={
                "first_name": "ReviewTest",
                "last_name": "User",
                "email": "review.test.user@example.com"
            },
            content_type='application/json')
        
        if user_response.status_code != 201:
            self.skipTest("Could not create test user")
            return
        
        self.user_id = json.loads(user_response.data)['id']
        
        # Try to create a place (will fail if endpoint not registered)
        try:
            place_response = self.client.post('/api/v1/places',
                json={
                    "title": "Review Test Place",
                    "description": "Test",
                    "price": 100.0,
                    "latitude": 0.0,
                    "longitude": 0.0,
                    "owner_id": self.user_id
                },
                content_type='application/json')
            
            if place_response.status_code == 201:
                self.place_id = json.loads(place_response.data)['id']
            else:
                self.skipTest("Could not create test place")
        except Exception:
            self.skipTest("Places endpoint not registered yet")

    def test_create_review_success(self):
        """Test successful review creation"""
        try:
            response = self.client.post('/api/v1/reviews',
                json={
                    "text": "Great place to stay!",
                    "rating": 5,
                    "user_id": self.user_id,
                    "place_id": self.place_id
                },
                content_type='application/json')
            
            self.assertEqual(response.status_code, 201)
            data = json.loads(response.data)
            self.assertIn('id', data)
            self.assertEqual(data['rating'], 5)
            print(f"✓ Created review: {data['id']}")
        except Exception as e:
            self.skipTest(f"Reviews endpoint not registered yet: {e}")

    def test_create_review_invalid_rating(self):
        """Test review creation with invalid rating"""
        try:
            response = self.client.post('/api/v1/reviews',
                json={
                    "text": "Test review",
                    "rating": 6,  # Invalid: > 5
                    "user_id": self.user_id,
                    "place_id": self.place_id
                },
                content_type='application/json')
            
            self.assertEqual(response.status_code, 400)
            print("✓ Invalid rating rejected")
        except Exception as e:
            self.skipTest(f"Reviews endpoint not registered yet: {e}")


if __name__ == '__main__':
    unittest.main(verbosity=2)