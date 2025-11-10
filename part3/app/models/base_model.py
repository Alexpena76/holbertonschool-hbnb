"""
BaseModel class for all entities
Provides common attributes and functionality
"""

from app import db  # SQLALCHEMY MAPPING: Import db instance
import uuid
from datetime import datetime


# SQLALCHEMY MAPPING: Now inherits from db.Model to become a SQLAlchemy model
class BaseModel(db.Model):
    """
    Base model class that provides common attributes for all entities.
    
    Attributes:
        id (str): Unique identifier (UUID)
        created_at (datetime): Timestamp when the object was created
        updated_at (datetime): Timestamp when the object was last updated
    
    SQLALCHEMY MAPPING: This class is now a SQLAlchemy model that will be
    inherited by all other entity models (User, Place, Review, Amenity).
    """
    
    # SQLALCHEMY MAPPING: Mark as abstract so SQLAlchemy doesn't create a table for BaseModel
    __abstract__ = True  # This ensures no "base_model" table is created
    
    # SQLALCHEMY MAPPING: Define database columns
    # Primary key - unique identifier for each record
    id = db.Column(
        db.String(36),  # UUID string length
        primary_key=True,  # This is the primary key
        default=lambda: str(uuid.uuid4())  # Auto-generate UUID
    )
    
    # SQLALCHEMY MAPPING: Timestamp columns with automatic defaults
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,  # Set to current time when created
        nullable=False
    )
    
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,  # Set to current time when created
        onupdate=datetime.utcnow,  # Update to current time when modified
        nullable=False
    )
    
    def save(self):
        """
        Save the current instance to the database
        
        SQLALCHEMY MAPPING: This method now commits to the database
        instead of just updating timestamps
        """
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
    
    def update(self, data):
        """
        Update the instance attributes with provided data
        
        Args:
            data (dict): Dictionary of attributes to update
        
        SQLALCHEMY MAPPING: After updating attributes, commits to database
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        """
        Convert instance to dictionary representation
        
        Returns:
            dict: Dictionary containing all attributes
        """
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }