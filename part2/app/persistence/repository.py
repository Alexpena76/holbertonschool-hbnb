"""
Repository Pattern Implementation
Provides abstract interface and concrete in-memory implementation
for data persistence operations
"""

from abc import ABC, abstractmethod


class Repository(ABC):
    """
    Abstract base class defining the repository interface
    
    This class establishes the contract that all repository
    implementations must follow, ensuring consistent data
    access patterns across different storage backends.
    """
    
    @abstractmethod
    def add(self, obj):
        """
        Store a new object in the repository
        
        Args:
            obj: Object to be stored (must have 'id' attribute)
        """
        pass

    @abstractmethod
    def get(self, obj_id):
        """
        Retrieve an object by its unique identifier
        
        Args:
            obj_id: Unique identifier of the object
            
        Returns:
            Object if found, None otherwise
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Retrieve all objects from the repository
        
        Returns:
            list: List of all stored objects
        """
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """
        Update an existing object with new data
        
        Args:
            obj_id: Unique identifier of the object to update
            data (dict): Dictionary containing fields to update
        """
        pass

    @abstractmethod
    def delete(self, obj_id):
        """
        Remove an object from the repository
        
        Args:
            obj_id: Unique identifier of the object to delete
        """
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """
        Find an object by a specific attribute value
        
        Args:
            attr_name (str): Name of the attribute to search
            attr_value: Value to match
            
        Returns:
            First matching object or None if not found
        """
        pass


class InMemoryRepository(Repository):
    """
    Concrete repository implementation using in-memory storage
    
    This implementation uses a Python dictionary to store objects
    in memory. It provides fast access but data is not persisted
    between application restarts.
    
    Storage Structure:
        self._storage = {obj_id: obj, ...}
    """
    
    def __init__(self):
        """Initialize empty storage dictionary"""
        self._storage = {}

    def add(self, obj):
        """
        Add an object to in-memory storage
        
        Args:
            obj: Object to store (must have 'id' attribute)
            
        Algorithm:
            1. Extract object ID
            2. Store object with ID as dictionary key
        """
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """
        Retrieve object by ID from storage
        
        Args:
            obj_id: Object identifier
            
        Returns:
            Object if found, None otherwise
            
        Algorithm:
            1. Use dict.get() for safe retrieval
            2. Return object or None if key doesn't exist
        """
        return self._storage.get(obj_id)

    def get_all(self):
        """
        Get all stored objects
        
        Returns:
            list: List of all objects in storage
            
        Algorithm:
            1. Extract all values from storage dictionary
            2. Convert dict_values to list
        """
        return list(self._storage.values())

    def update(self, obj_id, data):
        """
        Update existing object with new data
        
        Args:
            obj_id: Identifier of object to update
            data (dict): Dictionary of fields to update
            
        Algorithm:
            1. Retrieve object using get()
            2. If object exists, call its update() method
            3. Object's update() method handles field changes
        """
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """
        Remove object from storage
        
        Args:
            obj_id: Identifier of object to delete
            
        Algorithm:
            1. Check if ID exists in storage
            2. Delete dictionary entry if found
        """
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """
        Find first object matching attribute value
        
        Args:
            attr_name (str): Attribute name to search
            attr_value: Value to match
            
        Returns:
            First matching object or None
            
        Algorithm:
            1. Create generator iterating through all objects
            2. Use getattr() to safely access attribute
            3. Compare attribute value with search value
            4. Return first match using next()
        """
        return next(
            (obj for obj in self._storage.values() 
             if getattr(obj, attr_name) == attr_value),
            None
        )
