"""
Amenity-specific repository for database operations
Extends the generic SQLAlchemyRepository with amenity-specific queries
"""

from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository


class AmenityRepository(SQLAlchemyRepository):
    """
    Repository for Amenity entity with amenity-specific operations.
    
    This class extends SQLAlchemyRepository to provide amenity-specific
    database operations beyond basic CRUD functionality.
    
    SQLALCHEMY MAPPING: This repository handles all database interactions
    for the Amenity model.
    """
    
    def __init__(self):
        """
        Initialize AmenityRepository with Amenity model
        
        SQLALCHEMY MAPPING: Passes Amenity model to parent SQLAlchemyRepository
        so it knows which table to query.
        """
        super().__init__(Amenity)
    
    def get_by_name(self, name):
        """
        Retrieve an amenity by name
        
        Args:
            name (str): Amenity name to search for
            
        Returns:
            Amenity: Amenity object if found, None otherwise
        
        SQLALCHEMY MAPPING: Uses SQLAlchemy's filter_by to query the database.
        
        Example:
            amenity = amenity_repo.get_by_name('WiFi')
            if amenity:
                print(f"Found amenity: {amenity.name}")
        """
        return self.model.query.filter_by(name=name).first()