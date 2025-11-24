"""
Place Model
Represents a rental place in the HBnB application
"""

from app import db  # SQLALCHEMY MAPPING: Import db instance
from app.models.base_model import BaseModel


# SQLALCHEMY MAPPING: Place now inherits from BaseModel (which is a db.Model)
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
        owner_id (str): Foreign key to User
        owner (User): User who owns the place
        reviews (list): List of Review objects
        amenities (list): List of Amenity objects
        created_at (datetime): Creation timestamp
        updated_at (datetime): Last update timestamp
    
    Relationships:
        owner: Many-to-One with User (many places belong to one user)
        reviews: One-to-Many with Review (one place has many reviews)
        amenities: Many-to-Many with Amenity (place has many amenities)
    
    SQLALCHEMY MAPPING: This class is now a SQLAlchemy model that maps
    to the 'places' table in the database.
    """
    
    # SQLALCHEMY MAPPING: Define the table name
    __tablename__ = 'places'
    
    # SQLALCHEMY MAPPING: Define database columns with constraints
    title = db.Column(
        db.String(100),  # Maximum length 100 characters
        nullable=False  # Cannot be NULL
    )
    
    description = db.Column(
        db.String(1024),  # Maximum length 1024 characters
        nullable=True  # Can be NULL
    )
    
    price = db.Column(
        db.Float,  # Floating point number
        nullable=False  # Cannot be NULL
    )
    
    latitude = db.Column(
        db.Float,  # Floating point number
        nullable=False  # Cannot be NULL
    )
    
    longitude = db.Column(
        db.Float,  # Floating point number
        nullable=False  # Cannot be NULL
    )
    
    # FOREIGN KEY: Reference to User who owns this place
    owner_id = db.Column(
        db.String(36),  # UUID length
        db.ForeignKey('users.id'),  # RELATIONSHIP: Links to users table
        nullable=False  # Cannot be NULL
    )
    
    # ==================== RELATIONSHIPS ====================
    
    # RELATIONSHIP: Many-to-One with User
    # Many places can belong to one user
    # The backref 'owner' is defined in the User model (user.places)
    # This creates: place.owner -> User who owns this place
    # Usage example:
    #   place.owner -> returns the User object
    #   place.owner.email -> returns owner's email
    
    # RELATIONSHIP: One-to-Many with Review
    # One place can have many reviews
    reviews = db.relationship(
        'Review',  # The related model name
        backref='place',  # Creates reverse reference: review.place -> Place
        lazy=True,  # Load reviews when accessed (not automatically)
        cascade='all, delete-orphan'  # If place is deleted, delete all its reviews
    )
    # Usage examples:
    #   place.reviews -> list of all reviews for this place
    #   review.place -> the place being reviewed
    
    # RELATIONSHIP: Many-to-Many with Amenity
    # One place can have many amenities, one amenity can be in many places
    amenities = db.relationship(
        'Amenity',  # The related model name
        secondary='place_amenity',  # Association table name
        lazy='subquery',  # Load all amenities in one query when accessed
        backref=db.backref('places', lazy=True)  # Creates reverse: amenity.places
    )
    # Usage examples:
    #   place.amenities -> list of all Amenity objects for this place
    #   amenity.places -> list of all Place objects with this amenity
    
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        """
        Initialize a new Place
        
        Args:
            title (str): Place title
            description (str): Place description
            price (float): Price per night
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            owner_id (str): ID of the owner (SQLALCHEMY MAPPING: Changed from owner object to owner_id)
            
        Raises:
            ValueError: If validation fails
        
        SQLALCHEMY MAPPING: SQLAlchemy will automatically set id, created_at,
        and updated_at when this object is added to the database.
        
        RELATIONSHIPS: The reviews and amenities relationships are automatically
        initialized as empty lists by SQLAlchemy. No need to manually initialize them.
        """
        super().__init__()
        
        # Validate and set attributes
        self.title = self._validate_title(title)
        self.description = description if description else ""
        self.price = self._validate_price(price)
        self.latitude = self._validate_latitude(latitude)
        self.longitude = self._validate_longitude(longitude)
        self.owner_id = owner_id  # SQLALCHEMY MAPPING: Store owner_id instead of owner object
    
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
    
    def add_review(self, review):
        """
        Add a review to the place
        
        Args:
            review (Review): Review object to add
            
        Raises:
            ValueError: If review is invalid
        
        RELATIONSHIP: This method now works with the actual SQLAlchemy relationship.
        When you append a Review object to place.reviews, SQLAlchemy automatically
        manages the foreign key relationship in the database.
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
        
        RELATIONSHIP: This method now works with the actual SQLAlchemy relationship.
        When you append an Amenity object to place.amenities, SQLAlchemy automatically
        manages the many-to-many relationship through the place_amenity association table.
        """
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
            'owner_id': self.owner_id,  # SQLALCHEMY MAPPING: Return owner_id instead of owner.id
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }