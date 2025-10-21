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
        self.description = description  # Optional, no validation needed
        self.price = self._validate_price(price)
        self.latitude = self._validate_latitude(latitude)
        self.longitude = self._validate_longitude(longitude)
        self.owner = self._validate_owner(owner)
        
        # Initialize relationship lists
        self.reviews = []
        self.amenities = []
    
    def _validate_title(self, title):
        """Validate place title"""
        if not title or not isinstance(title, str):
            raise ValueError("Title is required and must be a string")
        if len(title) > 100:
            raise ValueError("Title must not exceed 100 characters")
        return title
    
    def _validate_price(self, price):
        """Validate price"""
        if not isinstance(price, (int, float)):
            raise ValueError("Price must be a number")
        if price <= 0:
            raise ValueError("Price must be a positive value")
        return float(price)
    
    def _validate_latitude(self, latitude):
        """Validate latitude coordinate"""
        if not isinstance(latitude, (int, float)):
            raise ValueError("Latitude must be a number")
        if latitude < -90.0 or latitude > 90.0:
            raise ValueError("Latitude must be between -90.0 and 90.0")
        return float(latitude)
    
    def _validate_longitude(self, longitude):
        """Validate longitude coordinate"""
        if not isinstance(longitude, (int, float)):
            raise ValueError("Longitude must be a number")
        if longitude < -180.0 or longitude > 180.0:
            raise ValueError("Longitude must be between -180.0 and 180.0")
        return float(longitude)
    
    def _validate_owner(self, owner):
        """Validate owner is a User instance"""
        from app.models.user import User
        if not isinstance(owner, User):
            raise ValueError("Owner must be a valid User instance")
        return owner
    
    def add_review(self, review):
        """
        Add a review to the place
        
        Args:
            review (Review): Review object to add
        """
        from app.models.review import Review
        if not isinstance(review, Review):
            raise ValueError("Must be a valid Review instance")
        self.reviews.append(review)
    
    def add_amenity(self, amenity):
        """
        Add an amenity to the place
        
        Args:
            amenity (Amenity): Amenity object to add
        """
        from app.models.amenity import Amenity
        if not isinstance(amenity, Amenity):
            raise ValueError("Must be a valid Amenity instance")
        if amenity not in self.amenities:
            self.amenities.append(amenity)
