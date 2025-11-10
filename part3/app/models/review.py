"""
Review Model
Represents a review for a place in the HBnB application
"""

from app import db  # SQLALCHEMY MAPPING: Import db instance
from app.models.base_model import BaseModel


# SQLALCHEMY MAPPING: Review now inherits from BaseModel (which is a db.Model)
class Review(BaseModel):
    """
    Review entity with validation and relationships
    
    Attributes:
        id (str): Unique identifier (UUID)
        text (str): Review content (required, max 1000 chars)
        rating (int): Rating from 1 to 5 (required)
        user_id (str): Foreign key to User
        place_id (str): Foreign key to Place
        user (User): User who wrote the review
        place (Place): Place being reviewed
        created_at (datetime): Creation timestamp
        updated_at (datetime): Last update timestamp
    
    Relationships:
        user: Many-to-One with User (many reviews belong to one user)
        place: Many-to-One with Place (many reviews belong to one place)
    
    SQLALCHEMY MAPPING: This class is now a SQLAlchemy model that maps
    to the 'reviews' table in the database.
    """
    
    # SQLALCHEMY MAPPING: Define the table name
    __tablename__ = 'reviews'
    
    # SQLALCHEMY MAPPING: Define database columns with constraints
    text = db.Column(
        db.String(1024),  # Maximum length 1024 characters (increased from 1000)
        nullable=False  # Cannot be NULL
    )
    
    rating = db.Column(
        db.Integer,  # Integer type
        nullable=False  # Cannot be NULL
    )
    
    # FOREIGN KEY: Reference to User who wrote this review
    user_id = db.Column(
        db.String(36),  # UUID length
        db.ForeignKey('users.id'),  # RELATIONSHIP: Links to users table
        nullable=False  # Cannot be NULL
    )
    
    # FOREIGN KEY: Reference to Place being reviewed
    place_id = db.Column(
        db.String(36),  # UUID length
        db.ForeignKey('places.id'),  # RELATIONSHIP: Links to places table
        nullable=False  # Cannot be NULL
    )
    
    # ==================== RELATIONSHIPS ====================
    
    # RELATIONSHIP: Many-to-One with User
    # Many reviews can be written by one user
    # The backref 'user' is defined in the User model (user.reviews)
    # This creates: review.user -> User who wrote this review
    # Usage example:
    #   review.user -> returns the User object
    #   review.user.email -> returns author's email
    
    # RELATIONSHIP: Many-to-One with Place
    # Many reviews can belong to one place
    # The backref 'place' is defined in the Place model (place.reviews)
    # This creates: review.place -> Place being reviewed
    # Usage example:
    #   review.place -> returns the Place object
    #   review.place.title -> returns place's title
    
    def __init__(self, text, rating, user_id, place_id):
        """
        Initialize a new Review
        
        Args:
            text (str): Review content
            rating (int): Rating (1-5)
            user_id (str): ID of the user (SQLALCHEMY MAPPING: Changed from user object)
            place_id (str): ID of the place (SQLALCHEMY MAPPING: Changed from place object)
            
        Raises:
            ValueError: If validation fails
        
        SQLALCHEMY MAPPING: SQLAlchemy will automatically set id, created_at,
        and updated_at when this object is added to the database.
        
        RELATIONSHIPS: The user and place relationships are automatically
        accessible through the backref defined in User and Place models.
        No manual initialization needed.
        """
        super().__init__()
        
        # Validate and set attributes
        self.text = self._validate_text(text)
        self.rating = self._validate_rating(rating)
        self.user_id = user_id  # SQLALCHEMY MAPPING: Store user_id instead of user object
        self.place_id = place_id  # SQLALCHEMY MAPPING: Store place_id instead of place object
    
    def _validate_text(self, text):
        """
        Validate review text
        
        Args:
            text (str): Review text to validate
            
        Returns:
            str: Validated and cleaned text
            
        Raises:
            ValueError: If text is invalid
        """
        if not text or not isinstance(text, str):
            raise ValueError("Review text is required and must be a string")
        
        # Check if text is not just whitespace
        if not text.strip():
            raise ValueError("Review text cannot be empty or just whitespace")
        
        # Check length
        if len(text.strip()) > 1000:
            raise ValueError("Review text must not exceed 1000 characters")
        
        return text.strip()
    
    def _validate_rating(self, rating):
        """
        Validate rating value
        
        Args:
            rating (int): Rating to validate
            
        Returns:
            int: Validated rating
            
        Raises:
            ValueError: If rating is invalid
        """
        if not isinstance(rating, int):
            raise ValueError("Rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating
    
    def to_dict(self):
        """
        Convert review to dictionary representation
        
        Returns:
            dict: Review data as dictionary
        """
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id,  # SQLALCHEMY MAPPING: Already have the ID
            'user_id': self.user_id,  # SQLALCHEMY MAPPING: Already have the ID
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }