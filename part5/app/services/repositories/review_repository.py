"""
Review-specific repository for database operations
Extends the generic SQLAlchemyRepository with review-specific queries
"""

from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository):
    """
    Repository for Review entity with review-specific operations.
    
    This class extends SQLAlchemyRepository to provide review-specific
    database operations beyond basic CRUD functionality.
    
    SQLALCHEMY MAPPING: This repository handles all database interactions
    for the Review model.
    """
    
    def __init__(self):
        """
        Initialize ReviewRepository with Review model
        
        SQLALCHEMY MAPPING: Passes Review model to parent SQLAlchemyRepository
        so it knows which table to query.
        """
        super().__init__(Review)
    
    def get_by_place(self, place_id):
        """
        Retrieve all reviews for a specific place
        
        Args:
            place_id (str): Place ID to search for
            
        Returns:
            list: List of Review objects for the place
        
        SQLALCHEMY MAPPING: Uses SQLAlchemy's filter_by to query the database.
        
        Example:
            reviews = review_repo.get_by_place('place-id-123')
            for review in reviews:
                print(f"Rating: {review.rating}/5 - {review.text}")
        """
        return self.model.query.filter_by(place_id=place_id).all()
    
    def get_by_user(self, user_id):
        """
        Retrieve all reviews written by a specific user
        
        Args:
            user_id (str): User ID to search for
            
        Returns:
            list: List of Review objects written by the user
        
        SQLALCHEMY MAPPING: Uses SQLAlchemy's filter_by to query the database.
        
        Example:
            reviews = review_repo.get_by_user('user-id-123')
            for review in reviews:
                print(f"Reviewed place: {review.place_id}")
        """
        return self.model.query.filter_by(user_id=user_id).all()