"""
Script to create an admin user
Run this once to create your first admin account

SQLALCHEMY MAPPING: Now creates admin in database instead of memory
"""

from app import create_app, db  # SQLALCHEMY MAPPING: Import db
from app.models.user import User
from app.services.facade import HBnBFacade


def create_admin_user():
    """
    Create an admin user for testing
    
    SQLALCHEMY MAPPING: Admin user is now saved to database
    """
    app = create_app()
    
    with app.app_context():
        facade = HBnBFacade()
        
        # Admin user data
        admin_data = {
            'first_name': 'Admin',
            'last_name': 'User',
            'email': 'admin@hbnb.com',
            'password': 'admin123',
            'is_admin': True  # This makes them an admin!
        }
        
        # SQLALCHEMY MAPPING: Check if admin exists in database
        existing_admin = facade.get_user_by_email(admin_data['email'])
        
        if existing_admin:
            print(f"❌ Admin user already exists: {admin_data['email']}")
            print(f"   User ID: {existing_admin.id}")
            print(f"   Is Admin: {existing_admin.is_admin}")
        else:
            # SQLALCHEMY MAPPING: Create admin user in database
            admin_user = facade.create_user(admin_data)
            print(f"✅ Admin user created successfully!")
            print(f"   Email: {admin_user.email}")
            print(f"   ID: {admin_user.id}")
            print(f"   Is Admin: {admin_user.is_admin}")
            print(f"\n📝 Login with:")
            print(f"   Email: {admin_data['email']}")
            print(f"   Password: {admin_data['password']}")


if __name__ == '__main__':
    create_admin_user()
