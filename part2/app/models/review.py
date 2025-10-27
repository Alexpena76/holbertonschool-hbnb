"""
Review Model
Represents a review for a place in the HBnB application
"""

from app.models.base_model import BaseModel


class Review(BaseModel):
    """
    Review entity with validation and relationships
    
    Attributes:
        id (str): Unique identifier (UUID)
        text (str): Review content (required, max 1000 chars)
        rating (int): Rating from 1 to 5 (required)
        place (Place): Place being reviewed
        user (User): User who wrote the review
        created_at (datetime): Creation timestamp
        updated_at (datetime): Last update timestamp
    """
    
    def __init__(self, text, rating, place, user):
        """
        Initialize a new Review
        
        Args:
            text (str): Review content
            rating (int): Rating (1-5)
            place (Place): Place being reviewed
            user (User): User who wrote the review
            
        Raises:
            ValueError: If validation fails
        """
        super().__init__()
        
        # Validate and set attributes
        self.text = self._validate_text(text)
        self.rating = self._validate_rating(rating)
        self.place = self._validate_place(place)
        self.user = self._validate_user(user)
    
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
    
    def _validate_place(self, place):
        """
        Validate place is a Place instance
        
        Args:
            place: Place object to validate
            
        Returns:
            Place: Validated place
            
        Raises:
            ValueError: If place is invalid
        """
        if not place:
            raise ValueError("Place is required")
        
        from app.models.place import Place
        if not isinstance(place, Place):
            raise ValueError("Place must be a valid Place instance")
        return place
    
    def _validate_user(self, user):
        """
        Validate user is a User instance
        
        Args:
            user: User object to validate
            
        Returns:
            User: Validated user
            
        Raises:
            ValueError: If user is invalid
        """
        if not user:
            raise ValueError("User is required")
        
        from app.models.user import User
        if not isinstance(user, User):
            raise ValueError("User must be a valid User instance")
        return user
    
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
            'place_id': self.place.id,
            'user_id': self.user.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }