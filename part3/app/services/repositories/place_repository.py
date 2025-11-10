"""
Place-specific repository for database operations
Extends the generic SQLAlchemyRepository with place-specific queries
"""

from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository


class PlaceRepository(SQLAlchemyRepository):
    """
    Repository for Place entity with place-specific operations.
    
    This class extends SQLAlchemyRepository to provide place-specific
    database operations beyond basic CRUD functionality.
    
    SQLALCHEMY MAPPING: This repository handles all database interactions
    for the Place model.
    """
    
    def __init__(self):
        """
        Initialize PlaceRepository with Place model
        
        SQLALCHEMY MAPPING: Passes Place model to parent SQLAlchemyRepository
        so it knows which table to query.
        """
        super().__init__(Place)
    
    def get_by_owner(self, owner_id):
        """
        Retrieve all places owned by a specific user
        
        Args:
            owner_id (str): User ID to search for
            
        Returns:
            list: List of Place objects owned by the user
        
        SQLALCHEMY MAPPING: Uses SQLAlchemy's filter_by to query the database.
        
        Example:
            places = place_repo.get_by_owner('user-id-123')
            for place in places:
                print(f"Place: {place.title}")
        """
        return self.model.query.filter_by(owner_id=owner_id).all()