"""
Base Model Class
Provides common attributes and methods for all entities
"""

import uuid
from datetime import datetime


class BaseModel:
    """
    Base class for all models in the application
    
    Provides common attributes:
        - id: Unique identifier (UUID)
        - created_at: Timestamp when object is created
        - updated_at: Timestamp when object is last modified
    """
    
    def __init__(self):
        """
        Initialize base model with UUID and timestamps
        
        Algorithm:
            1. Generate unique UUID and convert to string
            2. Set created_at to current datetime
            3. Set updated_at to current datetime
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """
        Update the updated_at timestamp
        
        Called whenever the object is modified to track
        the last modification time.
        """
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Update object attributes from dictionary
        
        Args:
            data (dict): Dictionary containing attribute names and values
            
        Algorithm:
            1. Iterate through dictionary items
            2. Check if attribute exists in object
            3. Update attribute value using setattr
            4. Call save() to update timestamp
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
