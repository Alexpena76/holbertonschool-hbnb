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

    # ==================== PLACE METHODS ====================
    
    def create_place(self, place_data):
        """Create a new place"""
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieve a place by ID"""
        return self.place_repo.get(place_id)
    
    def get_all_places(self):
        """Retrieve all places"""
        return self.place_repo.get_all()
    
    def update_place(self, place_id, place_data):
        """
        Update place information
        
        Args:
            place_id (str): Place's unique identifier
            place_data (dict): Dictionary containing fields to update
                - Can include amenity_ids to update amenities
                - Can include owner_id to change owner
        
        Returns:
            Place: Updated place object if found, None otherwise
            
        Raises:
            ValueError: If amenity not found
        """
        place = self.place_repo.get(place_id)
        if not place:
            return None
        
        # Handle owner_id if provided
        if 'owner_id' in place_data:
            owner_id = place_data.pop('owner_id')
            owner = self.get_user(owner_id)
            if owner:
                place.owner = owner
            else:
                raise ValueError("Owner not found")
        
        # Handle amenity_ids if provided
        if 'amenity_ids' in place_data:
            amenity_ids = place_data.pop('amenity_ids')
            
            # Clear existing amenities
            place.amenities = []
            
            # Add new amenities
            for amenity_id in amenity_ids:
                amenity = self.get_amenity(amenity_id)
                if amenity:
                    place.add_amenity(amenity)
                else:
                    raise ValueError(f"Amenity with ID {amenity_id} not found")
        
        # Update other fields (title, description, price, latitude, longitude)
        for key, value in place_data.items():
            if hasattr(place, key):
                setattr(place, key, value)
        
        # Update timestamp
        from datetime import datetime
        place.updated_at = datetime.now()
        
        return place

    # ==================== REVIEW METHODS ====================
    
    def create_place(self, place_data):
        """
        Create a new place
        
        Args:
            place_data (dict): Dictionary containing place information
                - title (str): Place title
                - description (str): Place description
                - price (float): Price per night
                - latitude (float): Latitude coordinate
                - longitude (float): Longitude coordinate
                - owner_id (str): ID of the place owner
        
        Returns:
            Place: Created place object
            
        Raises:
            ValueError: If validation fails or owner not found
        """
        # Extract owner_id from place_data
        owner_id = place_data.pop('owner_id')  # Remove owner_id from dict
        
        # Get the owner User object
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError("Owner not found")
        
        # Create place with owner object
        place = Place(**place_data, owner=owner)
        self.place_repo.add(place)
        return place
    
    def get_review(self, review_id):
        """Retrieve a review by ID"""
        return self.review_repo.get(review_id)
    
    def get_all_reviews(self):
        """Retrieve all reviews"""
        return self.review_repo.get_all()
    
    def update_review(self, review_id, review_data):
        """Update review information"""
        review = self.review_repo.get(review_id)
        if review:
            self.review_repo.update(review_id, review_data)
            return review
        return None

    # ==================== AMENITY METHODS ====================
    
    def create_amenity(self, amenity_data):
        """
        Create a new amenity
        
        Args:
            amenity_data (dict): Dictionary containing amenity information
            
        Returns:
            Amenity: The newly created amenity object
            
        Raises:
            ValueError: If the amenity data is invalid or amenity name already exists
        """
        # Validate that name is provided
        if 'name' not in amenity_data or not amenity_data['name']:
            raise ValueError("Amenity name is required")
        
        # Validate that name is not empty or just whitespace
        if not amenity_data['name'].strip():
            raise ValueError("Amenity name cannot be empty")
        
        # Check if amenity with the same name already exists
        existing_amenities = self.amenity_repo.get_all()
        for amenity in existing_amenities:
            if amenity.name.lower() == amenity_data['name'].strip().lower():
                raise ValueError("Amenity with this name already exists")
        
        # Create the new amenity
        new_amenity = Amenity(name=amenity_data['name'].strip())
        
        # Save to repository
        self.amenity_repo.add(new_amenity)
        
        return new_amenity

    def get_amenity(self, amenity_id):
        """
        Retrieve an amenity by ID
        
        Args:
            amenity_id (str): The UUID of the amenity
            
        Returns:
            Amenity: The amenity object if found, None otherwise
            
        Raises:
            ValueError: If the amenity is not found
        """
        amenity = self.amenity_repo.get(amenity_id)
        
        if not amenity:
            raise ValueError(f"Amenity with ID {amenity_id} not found")
        
        return amenity

    def get_all_amenities(self):
        """
        Retrieve all amenities
        
        Returns:
            list: List of all amenity objects
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an existing amenity
        
        Args:
            amenity_id (str): The UUID of the amenity to update
            amenity_data (dict): Dictionary containing updated amenity information
            
        Returns:
            Amenity: The updated amenity object
            
        Raises:
            ValueError: If the amenity is not found or data is invalid
        """
        # Validate that name is provided
        if 'name' not in amenity_data or not amenity_data['name']:
            raise ValueError("Amenity name is required")
        
        # Validate that name is not empty or just whitespace
        if not amenity_data['name'].strip():
            raise ValueError("Amenity name cannot be empty")
        
        # Retrieve the existing amenity
        amenity = self.amenity_repo.get(amenity_id)
        
        if not amenity:
            raise ValueError(f"Amenity with ID {amenity_id} not found")
        
        # Check if another amenity with the same name already exists (excluding current amenity)
        existing_amenities = self.amenity_repo.get_all()
        for existing_amenity in existing_amenities:
            if (existing_amenity.id != amenity_id and 
                existing_amenity.name.lower() == amenity_data['name'].strip().lower()):
                raise ValueError("Amenity with this name already exists")
        
        # Update the amenity's name
        amenity.name = amenity_data['name'].strip()
        
        # Save the updated amenity to the repository
        self.amenity_repo.update(amenity_id, amenity_data)
        
        return amenity

    def get_place(self, place_id):
        """Retrieve a place by ID"""
        return self.place_repo.get(place_id)
    
    def get_all_places(self):
        """Retrieve all places"""
        return self.place_repo.get_all()
    
    def update_place(self, place_id, place_data):
        """Update place information"""
        place = self.place_repo.get(place_id)
        if place:
            self.place_repo.update(place_id, place_data)
            return place
        return None
    
    def add_amenity_to_place(self, place_id, amenity_id):
        """
        Add an amenity to a place
        
        Args:
            place_id (str): Place's unique identifier
            amenity_id (str): Amenity's unique identifier
            
        Returns:
            Place: Updated place object
            
        Raises:
            ValueError: If place or amenity not found
        """
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        
        # Check if amenity already added
        if amenity in place.amenities:
            raise ValueError("Amenity already added to this place")
        
        # Add amenity to place
        place.add_amenity(amenity)
        
        return place

    # ==================== REVIEW METHODS ====================
    
    def create_review(self, review_data):
        """
        Create a new review
        
        Args:
            review_data (dict): Dictionary containing review information
                - text (str): Review text
                - rating (int): Rating (1-5)
                - user_id (str): ID of the user
                - place_id (str): ID of the place
        
        Returns:
            Review: Created review object
            
        Raises:
            ValueError: If validation fails
        """
        # Validate required fields
        if 'text' not in review_data or not review_data['text']:
            raise ValueError("Review text is required")
        
        if 'rating' not in review_data:
            raise ValueError("Rating is required")
        
        if 'user_id' not in review_data:
            raise ValueError("User ID is required")
        
        if 'place_id' not in review_data:
            raise ValueError("Place ID is required")
        
        # Get user and place objects
        user_id = review_data.pop('user_id')
        place_id = review_data.pop('place_id')
        
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        
        # Create review with user and place objects
        review = Review(**review_data, place=place, user=user)
        self.review_repo.add(review)
        
        # Add review to place's reviews list
        place.add_review(review)
        
        return review
    
    def get_reviews_by_place(self, place_id):
        """
        Retrieve all reviews for a specific place
        
        Args:
            place_id (str): Place's unique identifier
            
        Returns:
            list: List of Review objects for the place
            
        Raises:
            ValueError: If place not found
        """
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        
        return place.reviews
    
    def get_all_reviews(self):
        """Retrieve all reviews"""
        return self.review_repo.get_all()
    
    def update_review(self, review_id, review_data):
        """Update review information"""
        review = self.review_repo.get(review_id)
        if review:
            self.review_repo.update(review_id, review_data)
            return review
        return None

    def delete_review(self, review_id):
        """
        Delete a review
        
        Args:
            review_id (str): Review's unique identifier
            
        Raises:
            ValueError: If review not found
        """
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        
        # Remove review from place's reviews list
        if review in review.place.reviews:
            review.place.reviews.remove(review)
        
        # Delete from repository
        self.review_repo.delete(review_id)

    # ==================== AMENITY METHODS ====================
    
    def create_amenity(self, amenity_data):
        """
        Create a new amenity
        
        Args:
            amenity_data (dict): Dictionary containing amenity information
            
        Returns:
            Amenity: The newly created amenity object
            
        Raises:
            ValueError: If the amenity data is invalid or amenity name already exists
        """
        # Validate that name is provided
        if 'name' not in amenity_data or not amenity_data['name']:
            raise ValueError("Amenity name is required")
        
        # Validate that name is not empty or just whitespace
        if not amenity_data['name'].strip():
            raise ValueError("Amenity name cannot be empty")
        
        # Check if amenity with the same name already exists
        existing_amenities = self.amenity_repo.get_all()
        for amenity in existing_amenities:
            if amenity.name.lower() == amenity_data['name'].strip().lower():
                raise ValueError("Amenity with this name already exists")
        
        # Create the new amenity
        new_amenity = Amenity(name=amenity_data['name'].strip())
        
        # Save to repository
        self.amenity_repo.add(new_amenity)
        
        return new_amenity

    def get_amenity(self, amenity_id):
        """
        Retrieve an amenity by ID
        
        Args:
            amenity_id (str): The UUID of the amenity
            
        Returns:
            Amenity: The amenity object if found, None otherwise
            
        Raises:
            ValueError: If the amenity is not found
        """
        amenity = self.amenity_repo.get(amenity_id)
        
        if not amenity:
            raise ValueError(f"Amenity with ID {amenity_id} not found")
        
        return amenity

    def get_all_amenities(self):
        """
        Retrieve all amenities
        
        Returns:
            list: List of all amenity objects
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an existing amenity
        
        Args:
            amenity_id (str): The UUID of the amenity to update
            amenity_data (dict): Dictionary containing updated amenity information
            
        Returns:
            Amenity: The updated amenity object
            
        Raises:
            ValueError: If the amenity is not found or data is invalid
        """
        # Validate that name is provided
        if 'name' not in amenity_data or not amenity_data['name']:
            raise ValueError("Amenity name is required")
        
        # Validate that name is not empty or just whitespace
        if not amenity_data['name'].strip():
            raise ValueError("Amenity name cannot be empty")
        
        # Retrieve the existing amenity
        amenity = self.amenity_repo.get(amenity_id)
        
        if not amenity:
            raise ValueError(f"Amenity with ID {amenity_id} not found")
        
        # Check if another amenity with the same name already exists (excluding current amenity)
        existing_amenities = self.amenity_repo.get_all()
        for existing_amenity in existing_amenities:
            if (existing_amenity.id != amenity_id and 
                existing_amenity.name.lower() == amenity_data['name'].strip().lower()):
                raise ValueError("Amenity with this name already exists")
        
        # Update the amenity's name
        amenity.name = amenity_data['name'].strip()
        
        # Save the updated amenity to the repository
        self.amenity_repo.update(amenity_id, amenity_data)
        
        return amenity
