"""
Amenity Model
Represents an amenity (feature) in the HBnB application
"""

from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Amenity entity with validation
    
    Attributes:
        id (str): Unique identifier (UUID)
        name (str): Amenity name (max 50 chars, required)
        created_at (datetime): Creation timestamp
        updated_at (datetime): Last update timestamp
    
    Examples:
        - "Wi-Fi"
        - "Parking"
        - "Air Conditioning"
        - "Swimming Pool"
    """
    
    def __init__(self, name):
        """
        Initialize a new Amenity
        
        Args:
            name (str): Amenity name
            
        Raises:
            ValueError: If validation fails
        """
        super().__init__()
        self.name = self._validate_name(name)
    
    def _validate_name(self, name):
        """
        Validate amenity name
        
        Args:
            name (str): Name to validate
            
        Returns:
            str: Validated name
            
        Raises:
            ValueError: If name is invalid
        """
        if not name or not isinstance(name, str):
            raise ValueError("Amenity name is required and must be a string")
        if len(name) > 50:
            raise ValueError("Amenity name must not exceed 50 characters")
        return name
