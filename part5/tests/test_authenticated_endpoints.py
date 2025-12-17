"""
Comprehensive test suite for authenticated endpoints
Tests JWT authentication, ownership validation, and business rules
"""

import requests
import json

BASE_URL = "http://localhost:5000/api/v1"


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def test_authenticated_endpoints():
    """
    Test all authenticated endpoints with comprehensive scenarios
    
    This test covers:
    1. User creation and authentication
    2. Place creation and ownership validation
    3. Review creation with business rule validation
    4. Update and delete operations with ownership checks
    5. Public endpoint access without authentication
    """
    
    print("\n🧪 TESTING AUTHENTICATED ENDPOINTS")
    print("=" * 60)
    
    # ===== STEP 1: CREATE USERS =====
    print_section("1️⃣  Creating Test Users")
    
    user1_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.test@example.com",
        "password": "password123"
    }
    
    user2_data = {
        "first_name": "Bob",
        "last_name": "Jones",
        "email": "bob.test@example.com",
        "password": "password123"
    }
    
    # Create User 1 (Alice)
    print("Creating User 1 (Alice)...")
    response = requests.post(f"{BASE_URL}/users", json=user1_data)
    if response.status_code == 201:
        user1 = response.json()
        user1_id = user1['id']
        print(f"   ✓ User 1 created: {user1['email']}")
        print(f"     ID: {user1_id[:20]}...")
    elif "already registered" in response.text.lower():
        print(f"   ℹ User 1 already exists")
    else:
        print(f"   ✗ Failed: {response.text}")
    
    # Create User 2 (Bob)
    print("\nCreating User 2 (Bob)...")
    response = requests.post(f"{BASE_URL}/users", json=user2_data)
    if response.status_code == 201:
        user2 = response.json()
        user2_id = user2['id']
        print(f"   ✓ User 2 created: {user2['email']}")
        print(f"     ID: {user2_id[:20]}...")
    elif "already registered" in response.text.lower():
        print(f"   ℹ User 2 already exists")
    else:
        print(f"   ✗ Failed: {response.text}")
    
    # ===== STEP 2: LOGIN USERS =====
    print_section("2️⃣  Authenticating Users (Getting JWT Tokens)")
    
    # Login User 1 (Alice)
    print("Logging in User 1 (Alice)...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": user1_data["email"], "password": user1_data["password"]}
    )
    if response.status_code == 200:
        token1 = response.json()['access_token']
        headers1 = {"Authorization": f"Bearer {token1}"}
        print(f"   ✓ Login successful")
        print(f"     Token: {token1[:40]}...")
    else:
        print(f"   ✗ Login failed: {response.text}")
        return
    
    # Login User 2 (Bob)
    print("\nLogging in User 2 (Bob)...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": user2_data["email"], "password": user2_data["password"]}
    )
    if response.status_code == 200:
        token2 = response.json()['access_token']
        headers2 = {"Authorization": f"Bearer {token2}"}
        print(f"   ✓ Login successful")
        print(f"     Token: {token2[:40]}...")
    else:
        print(f"   ✗ Login failed: {response.text}")
        return
    
    # ===== STEP 3: CREATE PLACE =====
    print_section("3️⃣  User 1 Creating a Place")
    
    place_data = {
        "title": "Beautiful Beach House",
        "description": "A lovely beach house with ocean views",
        "price": 150.0,
        "latitude": 34.0522,
        "longitude": -118.2437,
        "owner_id": "this-will-be-overridden-by-jwt"
    }
    
    print("Creating place with User 1's token...")
    response = requests.post(f"{BASE_URL}/places", json=place_data, headers=headers1)
    if response.status_code == 201:
        place = response.json()
        place_id = place['id']
        print(f"   ✓ Place created successfully")
        print(f"     Title: {place['title']}")
        print(f"     ID: {place_id[:20]}...")
        print(f"     Owner: {place['owner_id'][:20]}...")
    else:
        print(f"   ✗ Failed to create place: {response.text}")
        return
    
    # ===== STEP 4: TEST PUBLIC ACCESS =====
    print_section("4️⃣  Testing Public Access (No Authentication)")
    
    print("Accessing GET /places without token...")
    response = requests.get(f"{BASE_URL}/places")
    if response.status_code == 200:
        places = response.json()
        print(f"   ✓ Public access granted")
        print(f"     Found {len(places)} place(s)")
    else:
        print(f"   ✗ Failed: {response.text}")
    
    print(f"\nAccessing GET /places/{place_id} without token...")
    response = requests.get(f"{BASE_URL}/places/{place_id}")
    if response.status_code == 200:
        place = response.json()
        print(f"   ✓ Public access granted")
        print(f"     Place: {place['title']}")
    else:
        print(f"   ✗ Failed: {response.text}")
    
    # ===== STEP 5: TEST UNAUTHORIZED UPDATE =====
    print_section("5️⃣  User 2 Attempting to Update User 1's Place (Should Fail)")
    
    update_data = {
        "title": "Hacked Place",
        "description": "This should not work",
        "price": 1.0,
        "latitude": 34.0522,
        "longitude": -118.2437,
        "owner_id": "ignored"
    }
    
    print("User 2 trying to update User 1's place...")
    response = requests.put(
        f"{BASE_URL}/places/{place_id}",
        json=update_data,
        headers=headers2
    )
    if response.status_code == 403:
        error = response.json()
        print(f"   ✓ Correctly rejected with 403")
        print(f"     Error: {error['error']}")
    else:
        print(f"   ✗ Should have been rejected!")
        print(f"     Response: {response.text}")
    
    # ===== STEP 6: TEST AUTHORIZED UPDATE =====
    print_section("6️⃣  User 1 Updating Own Place (Should Succeed)")
    
    update_data = {
        "title": "Updated Beach House",
        "description": "Now with updated description",
        "price": 175.0,
        "latitude": 34.0522,
        "longitude": -118.2437,
        "owner_id": "ignored"
    }
    
    print("User 1 updating own place...")
    response = requests.put(
        f"{BASE_URL}/places/{place_id}",
        json=update_data,
        headers=headers1
    )
    if response.status_code == 200:
        updated_place = response.json()
        print(f"   ✓ Place updated successfully")
        print(f"     New title: {updated_place['title']}")
        print(f"     New price: ${updated_place['price']}")
    else:
        print(f"   ✗ Failed to update place: {response.text}")
    
    # ===== STEP 7: TEST OWNER REVIEWING OWN PLACE =====
    print_section("7️⃣  User 1 Attempting to Review Own Place (Should Fail)")
    
    review_data = {
        "text": "This is my own place, it's great!",
        "rating": 5,
        "user_id": "will-be-overridden",
        "place_id": place_id
    }
    
    print("User 1 trying to review their own place...")
    response = requests.post(f"{BASE_URL}/reviews", json=review_data, headers=headers1)
    if response.status_code == 400 and "cannot review your own place" in response.text.lower():
        error = response.json()
        print(f"   ✓ Correctly rejected with 400")
        print(f"     Error: {error['error']}")
    else:
        print(f"   ✗ Should have been rejected!")
        print(f"     Response: {response.text}")
    
    # ===== STEP 8: TEST VALID REVIEW =====
    print_section("8️⃣  User 2 Reviewing User 1's Place (Should Succeed)")
    
    review_data = {
        "text": "Amazing place with great views!",
        "rating": 5,
        "user_id": "will-be-overridden",
        "place_id": place_id
    }
    
    print("User 2 creating review for User 1's place...")
    response = requests.post(f"{BASE_URL}/reviews", json=review_data, headers=headers2)
    if response.status_code == 201:
        review = response.json()
        review_id = review['id']
        print(f"   ✓ Review created successfully")
        print(f"     Text: {review['text']}")
        print(f"     Rating: {review['rating']} stars")
        print(f"     ID: {review_id[:20]}...")
    else:
        print(f"   ✗ Failed to create review: {response.text}")
        return
    
    # ===== STEP 9: TEST DUPLICATE REVIEW =====
    print_section("9️⃣  User 2 Attempting Duplicate Review (Should Fail)")
    
    duplicate_review = {
        "text": "Another review for the same place",
        "rating": 4,
        "user_id": "will-be-overridden",
        "place_id": place_id
    }
    
    print("User 2 trying to review the same place again...")
    response = requests.post(f"{BASE_URL}/reviews", json=duplicate_review, headers=headers2)
    if response.status_code == 400 and "already reviewed" in response.text.lower():
        error = response.json()
        print(f"   ✓ Correctly rejected with 400")
        print(f"     Error: {error['error']}")
    else:
        print(f"   ✗ Should have been rejected!")
        print(f"     Response: {response.text}")
    
    # ===== STEP 10: TEST UNAUTHORIZED REVIEW UPDATE =====
    print_section("🔟 User 1 Attempting to Update User 2's Review (Should Fail)")
    
    update_review = {
        "text": "I'm trying to modify someone else's review",
        "rating": 1,
        "user_id": "ignored",
        "place_id": place_id
    }
    
    print("User 1 trying to update User 2's review...")
    response = requests.put(
        f"{BASE_URL}/reviews/{review_id}",
        json=update_review,
        headers=headers1
    )
    if response.status_code == 403:
        error = response.json()
        print(f"   ✓ Correctly rejected with 403")
        print(f"     Error: {error['error']}")
    else:
        print(f"   ✗ Should have been rejected!")
        print(f"     Response: {response.text}")
    
    # ===== STEP 11: TEST AUTHORIZED REVIEW UPDATE =====
    print_section("1️⃣1️⃣  User 2 Updating Own Review (Should Succeed)")
    
    update_review = {
        "text": "Updated: Still an amazing place!",
        "rating": 5,
        "user_id": "ignored",
        "place_id": place_id
    }
    
    print("User 2 updating own review...")
    response = requests.put(
        f"{BASE_URL}/reviews/{review_id}",
        json=update_review,
        headers=headers2
    )
    if response.status_code == 200:
        updated_review = response.json()
        print(f"   ✓ Review updated successfully")
        print(f"     New text: {updated_review['text']}")
    else:
        print(f"   ✗ Failed to update review: {response.text}")
    
    # ===== STEP 12: TEST UNAUTHORIZED USER UPDATE =====
    print_section("1️⃣2️⃣  User 2 Attempting to Update User 1's Profile (Should Fail)")
    
    # First, get User 1's ID from login or create response
    # We need to extract it somehow - let's use the place owner_id
    print("User 2 trying to update User 1's profile...")
    response = requests.get(f"{BASE_URL}/auth/protected", headers=headers1)
    if response.status_code == 200:
        # This tells us User 1's ID
        pass
    
    user_update = {
        "first_name": "Hacked",
        "last_name": "Name",
        "email": "should-not-work@example.com",
        "password": "ignored"
    }
    
    # Try to update using the owner_id from the place
    response = requests.put(
        f"{BASE_URL}/users/{place['owner_id']}",
        json=user_update,
        headers=headers2
    )
    if response.status_code == 403:
        error = response.json()
        print(f"   ✓ Correctly rejected with 403")
        print(f"     Error: {error['error']}")
    else:
        print(f"   ✗ Should have been rejected!")
        print(f"     Response: {response.text}")
    
    # ===== STEP 13: TEST EMAIL/PASSWORD MODIFICATION =====
    print_section("1️⃣3️⃣  User 1 Attempting to Modify Email/Password (Should Fail)")
    
    user_update = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "newemail@example.com",  # This should be rejected
        "password": "newpassword"
    }
    
    print("User 1 trying to change email...")
    response = requests.put(
        f"{BASE_URL}/users/{place['owner_id']}",
        json=user_update,
        headers=headers1
    )
    if response.status_code == 400 and "cannot modify email or password" in response.text.lower():
        error = response.json()
        print(f"   ✓ Correctly rejected with 400")
        print(f"     Error: {error['error']}")
    else:
        print(f"   ✗ Should have been rejected!")
        print(f"     Response: {response.text}")
    
    # ===== STEP 14: TEST AUTHORIZED USER UPDATE =====
    print_section("1️⃣4️⃣  User 1 Updating Own Profile (Should Succeed)")
    
    user_update = {
        "first_name": "Alicia",
        "last_name": "Smith-Jones",
        "email": "ignored",
        "password": "ignored"
    }
    
    print("User 1 updating own profile...")
    response = requests.put(
        f"{BASE_URL}/users/{place['owner_id']}",
        json=user_update,
        headers=headers1
    )
    if response.status_code == 200:
        updated_user = response.json()
        print(f"   ✓ Profile updated successfully")
        print(f"     New name: {updated_user['first_name']} {updated_user['last_name']}")
    else:
        print(f"   ✗ Failed to update profile: {response.text}")
    
    # ===== STEP 15: TEST REVIEW DELETION =====
    print_section("1️⃣5️⃣  User 2 Deleting Own Review (Should Succeed)")
    
    print("User 2 deleting own review...")
    response = requests.delete(f"{BASE_URL}/reviews/{review_id}", headers=headers2)
    if response.status_code == 200:
        result = response.json()
        print(f"   ✓ Review deleted successfully")
        print(f"     Message: {result['message']}")
    else:
        print(f"   ✗ Failed to delete review: {response.text}")
    
    # ===== FINAL SUMMARY =====
    print_section("✅ TEST SUITE COMPLETED")
    print("All authenticated endpoint tests have been executed.")
    print("\nTested scenarios:")
    print("  ✓ User registration and authentication")
    print("  ✓ JWT token generation and validation")
    print("  ✓ Place creation with automatic owner assignment")
    print("  ✓ Public access to read-only endpoints")
    print("  ✓ Ownership validation for place updates")
    print("  ✓ Review creation with business rule validation")
    print("  ✓ Prevention of self-reviews and duplicate reviews")
    print("  ✓ Ownership validation for review updates and deletes")
    print("  ✓ User profile update restrictions")
    print("  ✓ Prevention of email/password modification")
    print("\n" + "=" * 60)


if __name__ == '__main__':
    try:
        test_authenticated_endpoints()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to the API")
        print("   Make sure the Flask app is running on http://localhost:5000")
        print("\n   Start the app with:")
        print("   $ python run.py")
    except KeyError as e:
        print(f"\n❌ ERROR: Missing expected data in response")
        print(f"   Key error: {e}")
        print("   This might indicate an API endpoint is not working correctly")
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()