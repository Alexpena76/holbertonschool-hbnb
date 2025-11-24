"""
Test password hashing functionality
"""

from app import create_app, bcrypt
from app.models.user import User


def test_password_hashing():
    """Test password hashing and verification"""
    app = create_app()
    
    with app.app_context():
        print("Testing password functionality...\n")
        
        # Test 1: Create user with password
        user = User(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password="securepassword123"
        )
        
        # Test 2: Check password is hashed
        assert user.password != "securepassword123"
        assert user.password.startswith('$2b$')
        print(f"✓ Password hashed successfully: {user.password[:30]}...")
        
        # Test 3: Verify correct password
        assert user.verify_password("securepassword123") is True
        print("✓ Correct password verified")
        
        # Test 4: Reject wrong password
        assert user.verify_password("wrongpassword") is False
        print("✓ Wrong password rejected")
        
        # Test 5: Check to_dict() excludes password
        user_dict = user.to_dict()
        assert 'password' not in user_dict
        print("✓ Password excluded from to_dict()")
        
        # Test 6: Check password validation
        try:
            user2 = User("Test", "User2", "test2@example.com", "short")
            assert False, "Should have raised ValueError for short password"
        except ValueError as e:
            assert "at least 6 characters" in str(e)
            print("✓ Short password rejected")
        
        print("\n✅ All password tests passed!")


if __name__ == '__main__':
    test_password_hashing()
