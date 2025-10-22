# ==================== FILE: app/services/facade.py ====================
"""
Facade Pattern Implementation - UPDATED
Provides a unified interface to coordinate operations across
business logic and persistence layers
"""

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    """
    Facade class that coordinates all business operations
    """
    
    def __init__(self):
        """Initialize facade with repository instances"""
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ==================== USER METHODS ====================
    
    def create_user(self, user_data):
        """
        Create a new user
        
        Args:
            user_data (dict): Dictionary containing user information
                - first_name (str): User's first name
                - last_name (str): User's last name
                - email (str): User's email address
                - is_admin (bool, optional): Admin flag
        
        Returns:
            User: Created user object
            
        Raises:
            ValueError: If validation fails
        """
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """
        Retrieve a user by ID
        
        Args:
            user_id (str): User's unique identifier
            
        Returns:
            User: User object if found, None otherwise
        """
        return self.user_repo.get(user_id)
    
    def get_all_users(self):
        """
        Retrieve all users
        
        Returns:
            list: List of all User objects
        """
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        """
        Find a user by email address
        
        Args:
            email (str): Email address to search for
            
        Returns:
            User: User object if found, None otherwise
        """
        return self.user_repo.get_by_attribute('email', email)
    
    def update_user(self, user_id, user_data):
        """
        Update user information
        
        Args:
            user_id (str): User's unique identifier
            user_data (dict): Dictionary containing fields to update
            
        Returns:
            User: Updated user object if found, None otherwise
        """
        user = self.user_repo.get(user_id)
        if user:
            # Validate email uniqueness if email is being updated
            if 'email' in user_data and user_data['email'] != user.email:
                existing_user = self.get_user_by_email(user_data['email'])
                if existing_user and existing_user.id != user_id:
                    raise ValueError("Email already registered")
            
            self.user_repo.update(user_id, user_data)
            return user
        return None

    # ==================== PLACE METHODS (Placeholders) ====================
    
    def create_place(self, place_data):
        """Create a new place (to be implemented)"""
        pass

    def get_place(self, place_id):
        """Retrieve a place by ID (to be implemented)"""
        pass
    
    def get_all_places(self):
        """Retrieve all places (to be implemented)"""
        pass
    
    def update_place(self, place_id, place_data):
        """Update place information (to be implemented)"""
        pass

    # ==================== REVIEW METHODS (Placeholders) ====================
    
    def create_review(self, review_data):
        """Create a new review (to be implemented)"""
        pass
    
    def get_review(self, review_id):
        """Retrieve a review by ID (to be implemented)"""
        pass
    
    def get_all_reviews(self):
        """Retrieve all reviews (to be implemented)"""
        pass
    
    def update_review(self, review_id, review_data):
        """Update review information (to be implemented)"""
        pass

    # ==================== AMENITY METHODS (Placeholders) ====================
    
    def create_amenity(self, amenity_data):
        """Create a new amenity (to be implemented)"""
        pass
    
    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID (to be implemented)"""
        pass
    
    def get_all_amenities(self):
        """Retrieve all amenities (to be implemented)"""
        pass
    
    def update_amenity(self, amenity_id, amenity_data):
        """Update amenity information (to be implemented)"""
        pass