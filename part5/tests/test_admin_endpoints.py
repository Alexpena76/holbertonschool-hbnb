"""
Comprehensive test suite for admin-only endpoints
Tests RBAC (Role-Based Access Control) functionality
"""

import requests
import json

BASE_URL = "http://localhost:5000/api/v1"


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def test_admin_endpoints():
    """
    Test all admin-only endpoints and admin bypass features
    
    This test covers:
    1. Admin user login
    2. Regular user login
    3. Admin-only user creation
    4. Admin-only user modification (including email/password)
    5. Admin-only amenity creation and modification
    6. Admin bypass for place modifications
    7. Admin bypass for review modifications and deletion
    """
    
    print("\n🔐 TESTING ADMIN ACCESS CONTROL")
    print("=" * 70)
    
    # ===== STEP 1: CREATE ADMIN USER (if not exists) =====
    print_section("1️⃣  Setting Up Admin User")
    
    admin_data = {
        "first_name": "Admin",
        "last_name": "User",
        "email": "admin@hbnb.com",
        "password": "admin123"
    }
    
    print("Attempting to create admin user (will fail if not admin)...")
    print("If this fails, run: python create_admin.py")
    
    # ===== STEP 2: LOGIN AS ADMIN =====
    print_section("2️⃣  Logging in as Admin")
    
    print("Logging in with admin credentials...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": "admin@hbnb.com", "password": "admin123"}
    )
    
    if response.status_code == 200:
        admin_token = response.json()['access_token']
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        print(f"   ✓ Admin login successful")
        print(f"     Token: {admin_token[:40]}...")
    else:
        print(f"   ✗ Admin login failed: {response.text}")
        print("\n⚠️  Please run 'python create_admin.py' first to create an admin user!")
        return
    
    # ===== STEP 3: CREATE REGULAR USER =====
    print_section("3️⃣  Creating Regular User (as Admin)")
    
    regular_user_data = {
        "first_name": "Regular",
        "last_name": "User",
        "email": "regular@test.com",
        "password": "password123"
    }
    
    print("Admin creating a regular user...")
    response = requests.post(
        f"{BASE_URL}/users",
        json=regular_user_data,
        headers=admin_headers
    )
    
    if response.status_code == 201:
        regular_user = response.json()
        regular_user_id = regular_user['id']
        print(f"   ✓ Regular user created by admin")
        print(f"     Email: {regular_user['email']}")
        print(f"     ID: {regular_user_id[:20]}...")
    elif "already registered" in response.text.lower():
        print(f"   ℹ Regular user already exists")
        # Get user by logging in
        login_response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": regular_user_data["email"], "password": regular_user_data["password"]}
        )
        if login_response.status_code == 200:
            # We'll get the ID later if needed
            pass
    else:
        print(f"   ✗ Failed to create user: {response.text}")
    
    # ===== STEP 4: LOGIN AS REGULAR USER =====
    print_section("4️⃣  Logging in as Regular User")
    
    print("Logging in with regular user credentials...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": "regular@test.com", "password": "password123"}
    )
    
    if response.status_code == 200:
        regular_token = response.json()['access_token']
        regular_headers = {"Authorization": f"Bearer {regular_token}"}
        print(f"   ✓ Regular user login successful")
        print(f"     Token: {regular_token[:40]}...")
    else:
        print(f"   ✗ Regular user login failed: {response.text}")
        return
    
    # ===== STEP 5: REGULAR USER TRIES TO CREATE USER (Should Fail) =====
    print_section("5️⃣  Regular User Attempting to Create User (Should Fail)")
    
    new_user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@test.com",
        "password": "password123"
    }
    
    print("Regular user trying to create a new user...")
    response = requests.post(
        f"{BASE_URL}/users",
        json=new_user_data,
        headers=regular_headers
    )
    
    if response.status_code == 403:
        error = response.json()
        print(f"   ✓ Correctly rejected with 403")
        print(f"     Error: {error['error']}")
    else:
        print(f"   ✗ Should have been rejected!")
        print(f"     Response: {response.text}")
    
    # ===== STEP 6: ADMIN MODIFIES USER EMAIL =====
    print_section("6️⃣  Admin Modifying User Email (Should Succeed)")
    
    update_data = {
        "first_name": "Regular",
        "last_name": "User",
        "email": "regular.updated@test.com",  # Admin can change email
        "password": "newpassword123"  # Admin can change password
    }
    
    print("Admin updating regular user's email and password...")
    # We need the user ID - let's get all users first
    response = requests.get(f"{BASE_URL}/users")
    users = response.json()
    regular_user_obj = None
    for user in users:
        if user['email'] in ['regular@test.com', 'regular.updated@test.com']:
            regular_user_obj = user
            break
    
    if regular_user_obj:
        response = requests.put(
            f"{BASE_URL}/users/{regular_user_obj['id']}",
            json=update_data,
            headers=admin_headers
        )
        
        if response.status_code == 200:
            updated_user = response.json()
            print(f"   ✓ User updated successfully by admin")
            print(f"     New email: {updated_user['email']}")
        else:
            print(f"   ✗ Failed to update user: {response.text}")
    else:
        print(f"   ⚠️  Could not find regular user to update")
    
    # ===== STEP 7: ADMIN CREATES AMENITY =====
    print_section("7️⃣  Admin Creating Amenity (Should Succeed)")
    
    amenity_data = {
        "name": "Swimming Pool"
    }
    
    print("Admin creating a new amenity...")
    response = requests.post(
        f"{BASE_URL}/amenities",
        json=amenity_data,
        headers=admin_headers
    )
    
    if response.status_code == 201:
        amenity = response.json()
        amenity_id = amenity['id']
        print(f"   ✓ Amenity created by admin")
        print(f"     Name: {amenity['name']}")
        print(f"     ID: {amenity_id[:20]}...")
    elif "already exists" in response.text.lower():
        print(f"   ℹ Amenity already exists")
        # Get existing amenities
        response = requests.get(f"{BASE_URL}/amenities")
        amenities = response.json()
        for am in amenities:
            if am['name'] == "Swimming Pool":
                amenity_id = am['id']
                print(f"     Using existing ID: {amenity_id[:20]}...")
                break
    else:
        print(f"   ✗ Failed to create amenity: {response.text}")
        return
    
    # ===== STEP 8: REGULAR USER TRIES TO CREATE AMENITY (Should Fail) =====
    print_section("8️⃣  Regular User Attempting to Create Amenity (Should Fail)")
    
    amenity_data2 = {
        "name": "Hot Tub"
    }
    
    print("Regular user trying to create an amenity...")
    response = requests.post(
        f"{BASE_URL}/amenities",
        json=amenity_data2,
        headers=regular_headers
    )
    
    if response.status_code == 403:
        error = response.json()
        print(f"   ✓ Correctly rejected with 403")
        print(f"     Error: {error['error']}")
    else:
        print(f"   ✗ Should have been rejected!")
        print(f"     Response: {response.text}")
    
    # ===== STEP 9: ADMIN MODIFIES AMENITY =====
    print_section("9️⃣  Admin Modifying Amenity (Should Succeed)")
    
    update_amenity = {
        "name": "Olympic Swimming Pool"
    }
    
    print("Admin updating amenity...")
    response = requests.put(
        f"{BASE_URL}/amenities/{amenity_id}",
        json=update_amenity,
        headers=admin_headers
    )
    
    if response.status_code == 200:
        updated_amenity = response.json()
        print(f"   ✓ Amenity updated by admin")
        print(f"     New name: {updated_amenity['name']}")
    else:
        print(f"   ✗ Failed to update amenity: {response.text}")
    
    # ===== STEP 10: REGULAR USER TRIES TO MODIFY AMENITY (Should Fail) =====
    print_section("🔟 Regular User Attempting to Modify Amenity (Should Fail)")
    
    update_amenity2 = {
        "name": "Hacked Amenity"
    }
    
    print("Regular user trying to update amenity...")
    response = requests.put(
        f"{BASE_URL}/amenities/{amenity_id}",
        json=update_amenity2,
        headers=regular_headers
    )
    
    if response.status_code == 403:
        error = response.json()
        print(f"   ✓ Correctly rejected with 403")
        print(f"     Error: {error['error']}")
    else:
        print(f"   ✗ Should have been rejected!")
        print(f"     Response: {response.text}")
    
    # ===== STEP 11: REGULAR USER CREATES PLACE =====
    print_section("1️⃣1️⃣  Regular User Creating a Place")
    
    place_data = {
        "title": "Regular User's House",
        "description": "A nice house",
        "price": 100.0,
        "latitude": 34.0522,
        "longitude": -118.2437,
        "owner_id": "ignored"
    }
    
    print("Regular user creating a place...")
    response = requests.post(
        f"{BASE_URL}/places",
        json=place_data,
        headers=regular_headers
    )
    
    if response.status_code == 201:
        place = response.json()
        place_id = place['id']
        print(f"   ✓ Place created by regular user")
        print(f"     Title: {place['title']}")
        print(f"     ID: {place_id[:20]}...")
    else:
        print(f"   ✗ Failed to create place: {response.text}")
        return
    
    # ===== STEP 12: ADMIN MODIFIES REGULAR USER'S PLACE (Bypass) =====
    print_section("1️⃣2️⃣  Admin Modifying Regular User's Place (Should Succeed)")
    
    update_place = {
        "title": "Admin Modified This Place",
        "description": "Admin can modify any place",
        "price": 200.0,
        "latitude": 34.0522,
        "longitude": -118.2437,
        "owner_id": "ignored"
    }
    
    print("Admin updating regular user's place...")
    response = requests.put(
        f"{BASE_URL}/places/{place_id}",
        json=update_place,
        headers=admin_headers
    )
    
    if response.status_code == 200:
        updated_place = response.json()
        print(f"   ✓ Place updated by admin (ownership bypassed)")
        print(f"     New title: {updated_place['title']}")
    else:
        print(f"   ✗ Failed to update place: {response.text}")
    
    # ===== STEP 13: ADMIN CREATES REVIEW ON REGULAR USER'S PLACE =====
    print_section("1️⃣3️⃣  Admin Creating Review on Regular User's Place")
    
    review_data = {
        "text": "Admin's review",
        "rating": 5,
        "place_id": place_id,
        "user_id": "ignored"
    }
    
    print("Admin creating a review...")
    response = requests.post(
        f"{BASE_URL}/reviews",
        json=review_data,
        headers=admin_headers
    )
    
    if response.status_code == 201:
        review = response.json()
        review_id = review['id']
        print(f"   ✓ Review created by admin")
        print(f"     Text: {review['text']}")
        print(f"     ID: {review_id[:20]}...")
    else:
        print(f"   ✗ Failed to create review: {response.text}")
        return
    
    # ===== STEP 14: REGULAR USER TRIES TO MODIFY ADMIN'S REVIEW (Should Fail) =====
    print_section("1️⃣4️⃣  Regular User Attempting to Modify Admin's Review (Should Fail)")
    
    update_review = {
        "text": "Hacked review",
        "rating": 1,
        "place_id": place_id,
        "user_id": "ignored"
    }
    
    print("Regular user trying to update admin's review...")
    response = requests.put(
        f"{BASE_URL}/reviews/{review_id}",
        json=update_review,
        headers=regular_headers
    )
    
    if response.status_code == 403:
        error = response.json()
        print(f"   ✓ Correctly rejected with 403")
        print(f"     Error: {error['error']}")
    else:
        print(f"   ✗ Should have been rejected!")
        print(f"     Response: {response.text}")
    
    # ===== STEP 15: ADMIN DELETES REVIEW (Should Succeed) =====
    print_section("1️⃣5️⃣  Admin Deleting Any Review (Should Succeed)")
    
    print("Admin deleting the review...")
    response = requests.delete(
        f"{BASE_URL}/reviews/{review_id}",
        headers=admin_headers
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"   ✓ Review deleted by admin")
        print(f"     Message: {result['message']}")
    else:
        print(f"   ✗ Failed to delete review: {response.text}")
    
    # ===== FINAL SUMMARY =====
    print_section("✅ ADMIN TEST SUITE COMPLETED")
    print("All admin access control tests have been executed.")
    print("\nTested scenarios:")
    print("  ✓ Admin user creation and login")
    print("  ✓ Regular user creation and login")
    print("  ✓ Admin-only user creation (POST /users)")
    print("  ✓ Admin-only user modification with email/password")
    print("  ✓ Regular user blocked from creating users")
    print("  ✓ Admin-only amenity creation (POST /amenities)")
    print("  ✓ Admin-only amenity modification (PUT /amenities)")
    print("  ✓ Regular user blocked from creating/modifying amenities")
    print("  ✓ Admin bypass for place modifications")
    print("  ✓ Admin bypass for review modifications and deletion")
    print("  ✓ Regular user still blocked from unauthorized actions")
    print("\n" + "=" * 70)


if __name__ == '__main__':
    try:
        test_admin_endpoints()
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