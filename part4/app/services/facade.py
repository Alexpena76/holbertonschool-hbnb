"""
Facade pattern implementation for business logic
Coordinates operations between models and repositories
"""

from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.services.repositories.user_repository import UserRepository  # SQLALCHEMY MAPPING: Database-backed
from app.services.repositories.amenity_repository import AmenityRepository  # SQLALCHEMY MAPPING: Database-backed
from app.services.repositories.place_repository import PlaceRepository  # SQLALCHEMY MAPPING: Database-backed
from app.services.repositories.review_repository import ReviewRepository  # SQLALCHEMY MAPPING: Database-backed


class HBnBFacade:
    """
    Facade class to manage business logic and coordinate between 
    different components of the application.
    
    Provides a simplified interface for:
    - User management (CRUD operations) - Database persistence
    - Amenity management (CRUD operations) - Database persistence
    - Place management (CRUD operations) - Database persistence
    - Review management (CRUD operations) - Database persistence
    
    SQLALCHEMY MAPPING: All operations now use database persistence.
    """
    
    def __init__(self):
        """
        Initialize repositories for different entities
        Each entity type has its own repository for data persistence
        
        SQLALCHEMY MAPPING: All entities now use database-backed repositories.
        """
        # SQLALCHEMY MAPPING: All repositories now use database
        self.user_repo = UserRepository()
        self.amenity_repo = AmenityRepository()  # SQLALCHEMY MAPPING: Changed from InMemoryRepository()
        self.place_repo = PlaceRepository()  # SQLALCHEMY MAPPING: Changed from InMemoryRepository()
        self.review_repo = ReviewRepository()  # SQLALCHEMY MAPPING: Changed from InMemoryRepository()
    
    # ==================== USER METHODS ====================
    
    def create_user(self, user_data):
        """
        Create a new user with hashed password
        
        Args:
            user_data (dict): Dictionary containing user information
                - first_name (str): User's first name
                - last_name (str): User's last name
                - email (str): User's email address (must be unique)
                - password (str): User's password (will be hashed)
                - is_admin (bool, optional): Admin status (default: False)
        
        Returns:
            User: The created user object
            
        Raises:
            ValueError: If email already exists or validation fails
            
        Example:
            user_data = {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'securepass123'
            }
            user = facade.create_user(user_data)
        
        SQLALCHEMY MAPPING: User is now saved to database instead of memory.
        """
        # SQLALCHEMY MAPPING: Check if email exists using database query
        email = user_data.get('email', '').strip().lower()
        existing_user = self.user_repo.get_user_by_email(email)
        
        if existing_user:
            raise ValueError('Email already registered')
        
        user = User(
            first_name=user_data.get('first_name'),
            last_name=user_data.get('last_name'),
            email=user_data.get('email'),
            password=user_data.get('password'),
            is_admin=user_data.get('is_admin', False)
        )
        
        # SQLALCHEMY MAPPING: Add to database
        self.user_repo.add(user)
        return user
    
    def get_user(self, user_id):
        """
        Retrieve a user by ID
        
        Args:
            user_id (str): The unique identifier of the user
            
        Returns:
            User: User object if found, None otherwise
            
        Example:
            user = facade.get_user('123e4567-e89b-12d3-a456-426614174000')
        
        SQLALCHEMY MAPPING: Queries database instead of memory.
        """
        return self.user_repo.get(user_id)
    
    def get_user_by_email(self, email):
        """
        Retrieve a user by email address
        
        Args:
            email (str): The email address to search for
            
        Returns:
            User: User object if found, None otherwise
            
        Example:
            user = facade.get_user_by_email('john@example.com')
        
        SQLALCHEMY MAPPING: Uses custom repository method to query database.
        """
        return self.user_repo.get_user_by_email(email.strip().lower())
    
    def get_all_users(self):
        """
        Retrieve all users
        
        Returns:
            list: List of all user objects
            
        Example:
            all_users = facade.get_all_users()
            for user in all_users:
                print(user.email)
        
        SQLALCHEMY MAPPING: Queries all users from database.
        """
        return self.user_repo.get_all()
    
    def update_user(self, user_id, user_data):
        """
        Update user information
        
        Args:
            user_id (str): The unique identifier of the user
            user_data (dict): Dictionary with fields to update
                - first_name (str, optional): New first name
                - last_name (str, optional): New last name
                - email (str, optional): New email (must be unique)
                - password (str, optional): New password (will be hashed)
                - is_admin (bool, optional): New admin status
            
        Returns:
            User: Updated user object if found, None otherwise
            
        Raises:
            ValueError: If email already exists or validation fails
            
        Example:
            updated_data = {
                'first_name': 'Jane',
                'email': 'jane@example.com',
                'password': 'newpassword123'
            }
            user = facade.update_user(user_id, updated_data)
        
        SQLALCHEMY MAPPING: Updates user in database.
        """
        # SQLALCHEMY MAPPING: Get user from database
        user = self.user_repo.get(user_id)
        if not user:
            return None
        
        # Update first name if provided
        if 'first_name' in user_data:
            user.first_name = user._validate_name(
                user_data['first_name'], 
                "First name"
            )
        
        # Update last name if provided
        if 'last_name' in user_data:
            user.last_name = user._validate_name(
                user_data['last_name'], 
                "Last name"
            )
        
        # Update email if provided (check for uniqueness)
        if 'email' in user_data:
            new_email = user._validate_email(user_data['email'])
            # SQLALCHEMY MAPPING: Check database for email conflicts
            existing_user = self.user_repo.get_user_by_email(new_email)
            if existing_user and existing_user.id != user_id:
                raise ValueError('Email already registered')
            user.email = new_email
        
        # Update password if provided (will be hashed)
        if 'password' in user_data:
            user.hash_password(user_data['password'])
        
        # Update admin status if provided
        if 'is_admin' in user_data:
            user.is_admin = user_data['is_admin']
        
        # SQLALCHEMY MAPPING: Commit changes to database
        self.user_repo.update(user_id, user_data)
        return user
    
    # ==================== AMENITY METHODS ====================
    
    def create_amenity(self, amenity_data):
        """
        Create a new amenity
        
        Args:
            amenity_data (dict): Dictionary containing amenity information
                - name (str): Amenity name (must be unique)
        
        Returns:
            Amenity: The created amenity object
            
        Raises:
            ValueError: If amenity name already exists or validation fails
            
        Example:
            amenity_data = {'name': 'WiFi'}
            amenity = facade.create_amenity(amenity_data)
        
        SQLALCHEMY MAPPING: Amenity is now saved to database instead of memory.
        """
        # SQLALCHEMY MAPPING: Check if amenity name exists in database
        amenity_name = amenity_data.get('name', '').strip()
        existing_amenity = self.amenity_repo.get_by_name(amenity_name)
        
        if existing_amenity:
            raise ValueError('Amenity name already exists')
        
        # Create amenity
        amenity = Amenity(name=amenity_data.get('name'))
        
        # SQLALCHEMY MAPPING: Add to database
        self.amenity_repo.add(amenity)
        return amenity
    
    def get_amenity(self, amenity_id):
        """
        Retrieve an amenity by ID
        
        Args:
            amenity_id (str): The unique identifier of the amenity
            
        Returns:
            Amenity: Amenity object if found, None otherwise
            
        Example:
            amenity = facade.get_amenity('123e4567-e89b-12d3-a456-426614174000')
        
        SQLALCHEMY MAPPING: Queries database instead of memory.
        """
        return self.amenity_repo.get(amenity_id)
    
    def get_all_amenities(self):
        """
        Retrieve all amenities
        
        Returns:
            list: List of all amenity objects
            
        Example:
            all_amenities = facade.get_all_amenities()
            for amenity in all_amenities:
                print(amenity.name)
        
        SQLALCHEMY MAPPING: Queries database instead of memory.
        """
        return self.amenity_repo.get_all()
    
    def update_amenity(self, amenity_id, amenity_data):
        """
        Update amenity information
        
        Args:
            amenity_id (str): The unique identifier of the amenity
            amenity_data (dict): Dictionary with fields to update
                - name (str): New amenity name (must be unique)
            
        Returns:
            Amenity: Updated amenity object if found, None otherwise
            
        Raises:
            ValueError: If new name already exists or validation fails
            
        Example:
            updated_data = {'name': 'High-Speed WiFi'}
            amenity = facade.update_amenity(amenity_id, updated_data)
        
        SQLALCHEMY MAPPING: Updates amenity in database.
        """
        # SQLALCHEMY MAPPING: Get amenity from database
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        
        if 'name' in amenity_data:
            new_name = amenity_data['name'].strip()
            
            # SQLALCHEMY MAPPING: Check database for name conflicts
            existing_amenity = self.amenity_repo.get_by_name(new_name)
            if existing_amenity and existing_amenity.id != amenity_id:
                raise ValueError('Amenity name already exists')
            
            # Validate and update name
            amenity.name = amenity._validate_name(new_name)
        
        # SQLALCHEMY MAPPING: Commit changes to database
        self.amenity_repo.update(amenity_id, amenity)
        return amenity
    
    # ==================== PLACE METHODS ====================
    
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
                - owner_id (str): ID of the user who owns the place
                - amenity_ids (list, optional): List of amenity IDs
        
        Returns:
            Place: The created place object
            
        Raises:
            ValueError: If owner doesn't exist or validation fails
            
        Example:
            place_data = {
                'title': 'Beach House',
                'description': 'Beautiful beach house',
                'price': 150.0,
                'latitude': 34.0522,
                'longitude': -118.2437,
                'owner_id': 'user-id-here'
            }
            place = facade.create_place(place_data)
        
        SQLALCHEMY MAPPING: Place is now saved to database. Owner validation checks database.
        RELATIONSHIPS: Now properly handles amenity relationships using Amenity objects.
        """
        # SQLALCHEMY MAPPING: Verify owner exists in database
        owner = self.user_repo.get(place_data.get('owner_id'))
        if not owner:
            raise ValueError('Owner not found')
        
        # Create place
        place = Place(
            title=place_data.get('title'),
            description=place_data.get('description'),
            price=place_data.get('price'),
            latitude=place_data.get('latitude'),
            longitude=place_data.get('longitude'),
            owner_id=place_data.get('owner_id')
        )
        
        # RELATIONSHIPS: Add amenities using the relationship (Amenity objects, not IDs)
        amenity_ids = place_data.get('amenity_ids', [])
        if amenity_ids:
            for amenity_id in amenity_ids:
                # SQLALCHEMY MAPPING: Get amenity object from database
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError(f'Amenity {amenity_id} not found')
                # RELATIONSHIPS: Add Amenity object (not ID) to place.amenities
                place.add_amenity(amenity)  # Changed: pass amenity object, not amenity_id
        
        # SQLALCHEMY MAPPING: Add to database
        self.place_repo.add(place)
        return place
    
    def get_place(self, place_id):
        """
        Retrieve a place by ID
        
        Args:
            place_id (str): The unique identifier of the place
            
        Returns:
            Place: Place object if found, None otherwise
            
        Example:
            place = facade.get_place('123e4567-e89b-12d3-a456-426614174000')
        
        SQLALCHEMY MAPPING: Queries database instead of memory.
        """
        return self.place_repo.get(place_id)
    
    def get_all_places(self):
        """
        Retrieve all places
        
        Returns:
            list: List of all place objects
            
        Example:
            all_places = facade.get_all_places()
            for place in all_places:
                print(place.title)
        
        SQLALCHEMY MAPPING: Queries database instead of memory.
        """
        return self.place_repo.get_all()
    
    def update_place(self, place_id, place_data):
        """
        Update place information
        
        Args:
            place_id (str): The unique identifier of the place
            place_data (dict): Dictionary with fields to update
                - title (str, optional): New title
                - description (str, optional): New description
                - price (float, optional): New price
                - latitude (float, optional): New latitude
                - longitude (float, optional): New longitude
                - amenity_ids (list, optional): New list of amenity IDs
            
        Returns:
            Place: Updated place object if found, None otherwise
            
        Raises:
            ValueError: If validation fails or amenities don't exist
            
        Example:
            updated_data = {
                'title': 'Luxury Beach House',
                'price': 200.0
            }
            place = facade.update_place(place_id, updated_data)
        
        SQLALCHEMY MAPPING: Updates place in database.
        RELATIONSHIPS: Now properly updates amenity relationships using Amenity objects.
        """
        # SQLALCHEMY MAPPING: Get place from database
        place = self.place_repo.get(place_id)
        if not place:
            return None
        
        # Update fields
        if 'title' in place_data:
            place.title = place._validate_title(place_data['title'])
        
        if 'description' in place_data:
            place.description = place_data['description']
        
        if 'price' in place_data:
            place.price = place._validate_price(place_data['price'])
        
        if 'latitude' in place_data:
            place.latitude = place._validate_latitude(place_data['latitude'])
        
        if 'longitude' in place_data:
            place.longitude = place._validate_longitude(place_data['longitude'])
        
        # RELATIONSHIPS: Update amenities using the relationship
        if 'amenity_ids' in place_data:
            amenity_ids = place_data['amenity_ids']
            
            # Verify all amenities exist and collect Amenity objects
            amenities = []
            for amenity_id in amenity_ids:
                # SQLALCHEMY MAPPING: Get amenity object from database
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError(f'Amenity {amenity_id} not found')
                amenities.append(amenity)
            
            # RELATIONSHIPS: Replace amenities list with Amenity objects
            # SQLAlchemy automatically handles the association table
            place.amenities = amenities  # Changed: assign list of Amenity objects
        
        # SQLALCHEMY MAPPING: Commit changes to database
        self.place_repo.update(place_id, place)
        return place
    
    # ==================== REVIEW METHODS ====================
    
    def create_review(self, review_data):
        """
        Create a new review
        
        Args:
            review_data (dict): Dictionary containing review information
                - text (str): Review text/content
                - rating (int): Rating from 1 to 5
                - user_id (str): ID of the user writing the review
                - place_id (str): ID of the place being reviewed
        
        Returns:
            Review: The created review object
            
        Raises:
            ValueError: If user or place doesn't exist, or validation fails
            
        Example:
            review_data = {
                'text': 'Great place!',
                'rating': 5,
                'user_id': 'user-id-here',
                'place_id': 'place-id-here'
            }
            review = facade.create_review(review_data)
        
        SQLALCHEMY MAPPING: Review is now saved to database. User and place validation checks database.
        """
        # SQLALCHEMY MAPPING: Verify user exists in database
        user = self.user_repo.get(review_data.get('user_id'))
        if not user:
            raise ValueError('User not found')
        
        # SQLALCHEMY MAPPING: Verify place exists in database
        place = self.place_repo.get(review_data.get('place_id'))
        if not place:
            raise ValueError('Place not found')
        
        # Create review
        review = Review(
            text=review_data.get('text'),
            rating=review_data.get('rating'),
            user_id=review_data.get('user_id'),
            place_id=review_data.get('place_id')
        )
        
        # SQLALCHEMY MAPPING: Add to database
        self.review_repo.add(review)
        return review
    
    def get_review(self, review_id):
        """
        Retrieve a review by ID
        
        Args:
            review_id (str): The unique identifier of the review
            
        Returns:
            Review: Review object if found, None otherwise
            
        Example:
            review = facade.get_review('123e4567-e89b-12d3-a456-426614174000')
        
        SQLALCHEMY MAPPING: Queries database instead of memory.
        """
        return self.review_repo.get(review_id)
    
    def get_all_reviews(self):
        """
        Retrieve all reviews
        
        Returns:
            list: List of all review objects
            
        Example:
            all_reviews = facade.get_all_reviews()
            for review in all_reviews:
                print(f"Rating: {review.rating}")
        
        SQLALCHEMY MAPPING: Queries database instead of memory.
        """
        return self.review_repo.get_all()
    
    def get_reviews_by_place(self, place_id):
        """
        Retrieve all reviews for a specific place
        
        Args:
            place_id (str): The unique identifier of the place
            
        Returns:
            list: List of review objects for the specified place
            
        Example:
            place_reviews = facade.get_reviews_by_place('place-id-here')
            avg_rating = sum(r.rating for r in place_reviews) / len(place_reviews)
        
        SQLALCHEMY MAPPING: Uses custom repository method to query database.
        """
        return self.review_repo.get_by_place(place_id)
    
    def update_review(self, review_id, review_data):
        """
        Update review information
        
        Args:
            review_id (str): The unique identifier of the review
            review_data (dict): Dictionary with fields to update
                - text (str, optional): New review text
                - rating (int, optional): New rating (1-5)
            
        Returns:
            Review: Updated review object if found, None otherwise
            
        Raises:
            ValueError: If validation fails
            
        Example:
            updated_data = {
                'text': 'Amazing place! Updated review.',
                'rating': 5
            }
            review = facade.update_review(review_id, updated_data)
        
        SQLALCHEMY MAPPING: Updates review in database.
        """
        # SQLALCHEMY MAPPING: Get review from database
        review = self.review_repo.get(review_id)
        if not review:
            return None
        
        # Update text if provided
        if 'text' in review_data:
            review.text = review._validate_text(review_data['text'])
        
        # Update rating if provided
        if 'rating' in review_data:
            review.rating = review._validate_rating(review_data['rating'])
        
        # SQLALCHEMY MAPPING: Commit changes to database
        self.review_repo.update(review_id, review)
        return review
    
    def delete_review(self, review_id):
        """
        Delete a review
        
        Args:
            review_id (str): The unique identifier of the review to delete
            
        Returns:
            bool: True if review was deleted, False if not found
            
        Example:
            success = facade.delete_review('review-id-here')
            if success:
                print("Review deleted successfully")
        
        SQLALCHEMY MAPPING: Deletes from database instead of memory.
        """
        return self.review_repo.delete(review_id)