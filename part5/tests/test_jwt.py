"""
Test JWT authentication functionality
"""

import requests
import json

BASE_URL = "http://localhost:5000/api/v1"


def test_jwt_flow():
    """Test the complete JWT authentication flow"""
    
    print("🧪 Testing JWT Authentication Flow\n")
    
    # Step 1: Create a test user
    print("1. Creating test user...")
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test.jwt@example.com",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    if response.status_code == 201:
        print("   ✓ User created successfully")
        user = response.json()
        print(f"   User ID: {user['id']}\n")
    elif "Email already registered" in response.text:
        print("   ℹ User already exists\n")
    else:
        print(f"   ✗ Failed to create user: {response.text}\n")
        return
    
    # Step 2: Login and get JWT token
    print("2. Logging in to get JWT token...")
    login_data = {
        "email": "test.jwt@example.com",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        print("   ✓ Login successful")
        token_data = response.json()
        access_token = token_data['access_token']
        print(f"   Token (first 50 chars): {access_token[:50]}...\n")
    else:
        print(f"   ✗ Login failed: {response.text}\n")
        return
    
    # Step 3: Access protected endpoint with token
    print("3. Accessing protected endpoint with token...")
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(f"{BASE_URL}/auth/protected", headers=headers)
    if response.status_code == 200:
        print("   ✓ Access granted")
        data = response.json()
        print(f"   Response: {json.dumps(data, indent=2)}\n")
    else:
        print(f"   ✗ Access denied: {response.text}\n")
    
    # Step 4: Try to access without token
    print("4. Trying to access protected endpoint without token...")
    response = requests.get(f"{BASE_URL}/auth/protected")
    if response.status_code == 401:
        print("   ✓ Correctly rejected - Missing token")
        print(f"   Error: {response.json()}\n")
    else:
        print(f"   ✗ Should have been rejected: {response.text}\n")
    
    # Step 5: Try with wrong credentials
    print("5. Testing with wrong credentials...")
    wrong_login = {
        "email": "test.jwt@example.com",
        "password": "wrongpassword"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=wrong_login)
    if response.status_code == 401:
        print("   ✓ Correctly rejected - Invalid credentials")
        print(f"   Error: {response.json()}\n")
    else:
        print(f"   ✗ Should have been rejected: {response.text}\n")
    
    print("✅ JWT Authentication tests completed!")


if __name__ == '__main__':
    try:
        test_jwt_flow()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API.")
        print("   Make sure the Flask app is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")