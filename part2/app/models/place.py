"""
Place Model
Represents a rental place in the HBnB application
"""

from app.models.base_model import BaseModel


class Place(BaseModel):
    """
    Place entity with validation and relationships
    
    Attributes:
        id (str): Unique identifier (UUID)
        title (str): Place title (max 100 chars, required)
        description (str): Place description (optional)
        price (float): Price per night (must be positive)
        latitude (float): Latitude coordinate (-90.0 to 90.0)
        longitude (float): Longitude coordinate (-180.0 to 180.0)
        owner (User): User who owns the place
        reviews (list): List of Review objects
        amenities (list): List of Amenity objects
        created_at (datetime): Creation timestamp
        updated_at (datetime): Last update timestamp
    """
    
    def __init__(self, title, description, price, latitude, longitude, owner):
        """
        Initialize a new Place
        
        Args:
            title (str): Place title
            description (str): Place description
            price (float): Price per night
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            owner (User): Owner of the place
            
        Raises:
            ValueError: If validation fails
        """
        super().__init__()
        
        # Validate and set attributes
        self.title = self._validate_title(title)
        self.description = description if description else ""
        self.price = self._validate_price(price)
        self.latitude = self._validate_latitude(latitude)
        self.longitude = self._validate_longitude(longitude)
        self.owner = self._validate_owner(owner)
        
        # Initialize relationship lists
        self.reviews = []
        self.amenities = []
    
    def _validate_title(self, title):
        """
        Validate place title
        
        Args:
            title (str): Title to validate
            
        Returns:
            str: Validated and cleaned title
            
        Raises:
            ValueError: If title is invalid
        """
        if not title or not isinstance(title, str):
            raise ValueError("Title is required and must be a string")
        
        # Check if title is not just whitespace
        if not title.strip():
            raise ValueError("Title cannot be empty or just whitespace")
        
        # Check length
        if len(title.strip()) > 100:
            raise ValueError("Title must not exceed 100 characters")
        
        return title.strip()
    
    def _validate_price(self, price):
        """
        Validate price
        
        Args:
            price: Price to validate
            
        Returns:
            float: Validated price
            
        Raises:
            ValueError: If price is invalid
        """
        if not isinstance(price, (int, float)):
            raise ValueError("Price must be a number")
        if price <= 0:
            raise ValueError("Price must be a positive value")
        return float(price)
    
    def _validate_latitude(self, latitude):
        """
        Validate latitude coordinate
        
        Args:
            latitude: Latitude to validate
            
        Returns:
            float: Validated latitude
            
        Raises:
            ValueError: If latitude is invalid
        """
        if not isinstance(latitude, (int, float)):
            raise ValueError("Latitude must be a number")
        if latitude < -90.0 or latitude > 90.0:
            raise ValueError("Latitude must be between -90.0 and 90.0")
        return float(latitude)
    
    def _validate_longitude(self, longitude):
        """
        Validate longitude coordinate
        
        Args:
            longitude: Longitude to validate
            
        Returns:
            float: Validated longitude
            
        Raises:
            ValueError: If longitude is invalid
        """
        if not isinstance(longitude, (int, float)):
            raise ValueError("Longitude must be a number")
        if longitude < -180.0 or longitude > 180.0:
            raise ValueError("Longitude must be between -180.0 and 180.0")
        return float(longitude)
    
    def _validate_owner(self, owner):
        """
        Validate owner is a User instance
        
        Args:
            owner: Owner to validate
            
        Returns:
            User: Validated owner
            
        Raises:
            ValueError: If owner is invalid
        """
        if not owner:
            raise ValueError("Owner is required")
        
        from app.models.user import User
        if not isinstance(owner, User):
            raise ValueError("Owner must be a valid User instance")
        return owner
    
    def add_review(self, review):
        """
        Add a review to the place
        
        Args:
            review (Review): Review object to add
            
        Raises:
            ValueError: If review is invalid
        """
        from app.models.review import Review
        if not isinstance(review, Review):
            raise ValueError("Must be a valid Review instance")
        if review not in self.reviews:
            self.reviews.append(review)
    
    def add_amenity(self, amenity):
        """
        Add an amenity to the place
        
        Args:
            amenity (Amenity): Amenity object to add
            
        Raises:
            ValueError: If amenity is invalid
        """
        from app.models.amenity import Amenity
        if not isinstance(amenity, Amenity):
            raise ValueError("Must be a valid Amenity instance")
        if amenity not in self.amenities:
            self.amenities.append(amenity)
    
    def to_dict(self):
        """
        Convert place to dictionary representation
        
        Returns:
            dict: Place data as dictionary
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'amenities': [
                {
                    'id': amenity.id,
                    'name': amenity.name
                }
                for amenity in self.amenities
            ],
            'reviews': [
                {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user.id
                }
                for review in self.reviews
            ]
        }