"""
Amenity model for place amenities
"""

from app import db  # SQLALCHEMY MAPPING: Import db instance
from app.models.base_model import BaseModel


# SQLALCHEMY MAPPING: Amenity now inherits from BaseModel (which is a db.Model)
class Amenity(BaseModel):
    """
    Amenity entity representing place amenities.
    
    Attributes:
        id (str): Unique identifier (UUID)
        name (str): Amenity name (unique)
        created_at (datetime): Creation timestamp
        updated_at (datetime): Last update timestamp
    
    Relationships:
        places: Many-to-Many with Place (amenity can be in many places)
    
    SQLALCHEMY MAPPING: This class is now a SQLAlchemy model that maps
    to the 'amenities' table in the database.
    """
    
    # SQLALCHEMY MAPPING: Define the table name
    __tablename__ = 'amenities'
    
    # SQLALCHEMY MAPPING: Define database columns with constraints
    name = db.Column(
        db.String(50),  # Maximum length 50 characters
        nullable=False,  # Cannot be NULL
        unique=True  # Must be unique across all amenities
    )
    
    # ==================== RELATIONSHIPS ====================
    
    # RELATIONSHIP: Many-to-Many with Place
    # One amenity can be in many places, one place can have many amenities
    # The relationship is defined in the Place model (place.amenities)
    # The backref 'places' is created by Place.amenities
    # This creates: amenity.places -> list of Place objects
    # Usage example:
    #   amenity.places -> returns list of all places with this amenity
    #   place.amenities -> returns list of all amenities in this place
    
    # Note: No db.relationship() code here!
    # The relationship exists through:
    # 1. The 'place_amenity' association table (defined in app/models/__init__.py)
    # 2. The backref in Place.amenities (defined in app/models/place.py)
    # This is the same pattern as Review - backref creates amenity.places automatically!
    
    def __init__(self, name):
        """
        Initialize an Amenity instance
        
        Args:
            name (str): Amenity name
            
        Raises:
            ValueError: If validation fails
        
        SQLALCHEMY MAPPING: SQLAlchemy will automatically set id, created_at,
        and updated_at when this object is added to the database.
        
        RELATIONSHIPS: The places relationship is automatically accessible
        through the backref defined in Place.amenities. No manual initialization needed.
        """
        # Validate and set name
        self.name = self._validate_name(name)
    
    def _validate_name(self, name):
        """
        Validate amenity name
        
        Args:
            name (str): Name to validate
            
        Returns:
            str: Validated and cleaned name
            
        Raises:
            ValueError: If validation fails
        """
        if not name or not isinstance(name, str):
            raise ValueError("Amenity name is required and must be a string")
        
        name = name.strip()
        
        if len(name) == 0:
            raise ValueError("Amenity name cannot be empty")
        
        if len(name) > 50:
            raise ValueError("Amenity name must be less than 50 characters")
        
        return name
    
    def to_dict(self):
        """
        Convert amenity instance to dictionary
        
        Returns:
            dict: Amenity data
        """
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }