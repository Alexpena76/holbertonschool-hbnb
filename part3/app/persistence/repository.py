"""
Repository pattern implementation for data persistence
Provides both in-memory and SQLAlchemy-based repositories
"""

from abc import ABC, abstractmethod
from app import db  # SQLALCHEMY ADDITION: Import db instance


class Repository(ABC):
    """
    Abstract base class for repository pattern.
    Defines the interface that all repositories must implement.
    """
    
    @abstractmethod
    def add(self, obj):
        """Add a new object to the repository"""
        pass
    
    @abstractmethod
    def get(self, obj_id):
        """Retrieve an object by its ID"""
        pass
    
    @abstractmethod
    def get_all(self):
        """Retrieve all objects"""
        pass
    
    @abstractmethod
    def update(self, obj_id, data):
        """Update an object"""
        pass
    
    @abstractmethod
    def delete(self, obj_id):
        """Delete an object"""
        pass
    
    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve an object by a specific attribute"""
        pass


class InMemoryRepository(Repository):
    """
    In-memory repository implementation using a dictionary.
    Used for development and testing without a database.
    """
    
    def __init__(self):
        """Initialize the in-memory storage"""
        self._storage = {}
    
    def add(self, obj):
        """
        Add an object to the in-memory storage
        
        Args:
            obj: Object with an 'id' attribute
        """
        self._storage[obj.id] = obj
    
    def get(self, obj_id):
        """
        Retrieve an object by ID
        
        Args:
            obj_id (str): Object's unique identifier
            
        Returns:
            Object if found, None otherwise
        """
        return self._storage.get(obj_id)
    
    def get_all(self):
        """
        Retrieve all objects
        
        Returns:
            list: List of all objects in storage
        """
        return list(self._storage.values())
    
    def update(self, obj_id, data):
        """
        Update an object with new data
        
        Args:
            obj_id (str): Object's unique identifier
            data (dict): Dictionary of attributes to update
            
        Returns:
            Updated object if found, None otherwise
        """
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
        return obj
    
    def delete(self, obj_id):
        """
        Delete an object by ID
        
        Args:
            obj_id (str): Object's unique identifier
            
        Returns:
            bool: True if deleted, False if not found
        """
        if obj_id in self._storage:
            del self._storage[obj_id]
            return True
        return False
    
    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve an object by a specific attribute
        
        Args:
            attr_name (str): Name of the attribute
            attr_value: Value to match
            
        Returns:
            First object matching the criteria, None if not found
        """
        for obj in self._storage.values():
            if getattr(obj, attr_name, None) == attr_value:
                return obj
        return None


# SQLALCHEMY ADDITION: New SQLAlchemy-based repository implementation
class SQLAlchemyRepository(Repository):
    """
    SQLAlchemy-based repository implementation.
    Persists data to a relational database using SQLAlchemy ORM.
    
    This repository provides the same interface as InMemoryRepository
    but stores data in a database instead of memory.
    """
    
    def __init__(self, model):
        """
        Initialize the repository with a SQLAlchemy model
        
        Args:
            model: SQLAlchemy model class (e.g., User, Place, Review)
        """
        self.model = model
    
    def add(self, obj):
        """
        Add an object to the database
        
        Args:
            obj: SQLAlchemy model instance
        """
        db.session.add(obj)
        db.session.commit()
    
    def get(self, obj_id):
        """
        Retrieve an object by ID from the database
        
        Args:
            obj_id (str): Object's unique identifier
            
        Returns:
            Object if found, None otherwise
        """
        return self.model.query.get(obj_id)
    
    def get_all(self):
        """
        Retrieve all objects from the database
        
        Returns:
            list: List of all objects
        """
        return self.model.query.all()
    
    def update(self, obj_id, data):
        """
        Update an object in the database
        
        Args:
            obj_id (str): Object's unique identifier
            data (dict): Dictionary of attributes to update
            
        Returns:
            Updated object if found, None otherwise
        """
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
        return obj
    
    def delete(self, obj_id):
        """
        Delete an object from the database
        
        Args:
            obj_id (str): Object's unique identifier
            
        Returns:
            bool: True if deleted, False if not found
        """
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False
    
    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve an object by a specific attribute from the database
        
        Args:
            attr_name (str): Name of the attribute
            attr_value: Value to match
            
        Returns:
            First object matching the criteria, None if not found
        """
        return self.model.query.filter_by(**{attr_name: attr_value}).first()