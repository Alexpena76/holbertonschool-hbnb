"""
Test Password Hashing Functionality
"""

from app import create_app, db
from app.models.user import User


def test_password_hashing():
    """Test password hashing and verification"""
    app = create_app('config.TestingConfig')
    
    with app.app_context():
        db.create_all()
        
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
        
        # Test 5: Save to DB and check to_dict() excludes password
        db.session.add(user)
        db.session.commit()
        
        user_dict = user.to_dict()
        assert 'password' not in user_dict
        assert 'id' in user_dict
        assert 'created_at' in user_dict
        print("✓ to_dict() excludes password")
        
        print("\n✅ All password tests passed!")
        
        # Cleanup
        db.drop_all()


if __name__ == '__main__':
    test_password_hashing()