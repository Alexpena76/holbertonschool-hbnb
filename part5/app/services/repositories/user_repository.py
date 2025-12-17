"""
User-specific repository for database operations
Extends the generic SQLAlchemyRepository with user-specific queries
"""

from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """
    Repository for User entity with user-specific operations.
    
    This class extends SQLAlchemyRepository to provide user-specific
    database operations beyond basic CRUD functionality.
    
    SQLALCHEMY MAPPING: This repository handles all database interactions
    for the User model, including custom queries like finding users by email.
    """
    
    def __init__(self):
        """
        Initialize UserRepository with User model
        
        SQLALCHEMY MAPPING: Passes User model to parent SQLAlchemyRepository
        so it knows which table to query.
        """
        super().__init__(User)
    
    def get_user_by_email(self, email):
        """
        Retrieve a user by their email address
        
        Args:
            email (str): Email address to search for
            
        Returns:
            User: User object if found, None otherwise
        
        SQLALCHEMY MAPPING: Uses SQLAlchemy's filter_by to query the database.
        This is a user-specific operation that wouldn't belong in the generic repository.
        
        Example:
            user = user_repo.get_user_by_email('john@example.com')
            if user:
                print(f"Found user: {user.first_name}")
        """
        return self.model.query.filter_by(email=email).first()