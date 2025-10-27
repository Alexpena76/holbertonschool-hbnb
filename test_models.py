"""
Test Script for Business Logic Models
Run this to verify all models work correctly
"""

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


def test_user_creation():
    """Test User model creation and validation"""
    print("Testing User creation...")
    
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False
    assert user.id is not None
    
    print("✓ User creation test passed!")


def test_place_creation():
    """Test Place model creation with relationships"""
    print("Testing Place creation...")
    
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(
        title="Cozy Apartment",
        description="A nice place to stay",
        price=100.0,
        latitude=37.7749,
        longitude=-122.4194,
        owner=owner
    )
    
    assert place.title == "Cozy Apartment"
    assert place.price == 100.0
    assert place.owner == owner
    assert len(place.reviews) == 0
    assert len(place.amenities) == 0
    
    print("✓ Place creation test passed!")


def test_review_creation():
    """Test Review model creation and relationships"""
    print("Testing Review creation...")
    
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(
        title="Cozy Apartment",
        description="A nice place to stay",
        price=100.0,
        latitude=37.7749,
        longitude=-122.4194,
        owner=owner
    )
    
    reviewer = User(first_name="Bob", last_name="Johnson", email="bob.j@example.com")
    review = Review(text="Great stay!", rating=5, place=place, user=reviewer)
    
    place.add_review(review)
    
    assert review.text == "Great stay!"
    assert review.rating == 5
    assert review.place == place
    assert review.user == reviewer
    assert len(place.reviews) == 1
    assert place.reviews[0] == review
    
    print("✓ Review creation and relationship test passed!")


def test_amenity_creation():
    """Test Amenity model creation"""
    print("Testing Amenity creation...")
    
    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"
    assert amenity.id is not None
    
    print("✓ Amenity creation test passed!")


def test_place_amenities():
    """Test Place-Amenity many-to-many relationship"""
    print("Testing Place-Amenity relationship...")
    
    owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
    place = Place(
        title="Beach House",
        description="Beautiful beach house",
        price=200.0,
        latitude=34.0522,
        longitude=-118.2437,
        owner=owner
    )
    
    wifi = Amenity(name="Wi-Fi")
    parking = Amenity(name="Parking")
    pool = Amenity(name="Swimming Pool")
    
    place.add_amenity(wifi)
    place.add_amenity(parking)
    place.add_amenity(pool)
    
    assert len(place.amenities) == 3
    assert wifi in place.amenities
    assert parking in place.amenities
    assert pool in place.amenities
    
    print("✓ Place-Amenity relationship test passed!")


def test_update_method():
    """Test the update method from BaseModel"""
    print("Testing update method...")
    
    user = User(first_name="John", last_name="Doe", email="john@example.com")
    original_updated_at = user.updated_at
    
    import time
    time.sleep(0.1)  # Small delay to ensure timestamp changes
    
    user.update({"first_name": "Jane", "last_name": "Smith"})
    
    assert user.first_name == "Jane"
    assert user.last_name == "Smith"
    assert user.email == "john@example.com"  # Should not change
    assert user.updated_at > original_updated_at
    
    print("✓ Update method test passed!")


def run_all_tests():
    """Run all test functions"""
    print("\n" + "="*50)
    print("Running HBnB Business Logic Tests")
    print("="*50 + "\n")
    
    try:
        test_user_creation()
        test_place_creation()
        test_review_creation()
        test_amenity_creation()
        test_place_amenities()
        test_update_method()
        
        print("\n" + "="*50)
        print("✓ ALL TESTS PASSED!")
        print("="*50 + "\n")
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}\n")
    except Exception as e:
        print(f"\n✗ Error: {e}\n")


if __name__ == "__main__":
    run_all_tests()