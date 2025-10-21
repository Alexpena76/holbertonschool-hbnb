"""
User Model
Represents a user in the HBnB application
"""

from app.models.base_model import BaseModel


class User(BaseModel):
    """
    User entity with validation
    
    Attributes:
        id (str): Unique identifier (UUID)
        first_name (str): User's first name (max 50 chars, required)
        last_name (str): User's last name (max 50 chars, required)
        email (str): User's email address (unique, required)
        is_admin (bool): Administrative privileges flag (default: False)
        created_at (datetime): Creation timestamp
        updated_at (datetime): Last update timestamp
    """
    
    def __init__(self, first_name, last_name, email, is_admin=False):
        """
        Initialize a new User
        
        Args:
            first_name (str): User's first name
            last_name (str): User's last name
            email (str): User's email address
            is_admin (bool): Admin flag (default: False)
            
        Raises:
            ValueError: If validation fails
        """
        super().__init__()
        
        # Validate and set attributes
        self.first_name = self._validate_name(first_name, "First name")
        self.last_name = self._validate_name(last_name, "Last name")
        self.email = self._validate_email(email)
        self.is_admin = is_admin
    
    def _validate_name(self, name, field_name):
        """
        Validate name fields
        
        Args:
            name (str): Name to validate
            field_name (str): Field name for error messages
            
        Returns:
            str: Validated name
            
        Raises:
            ValueError: If name is invalid
        """
        if not name or not isinstance(name, str):
            raise ValueError(f"{field_name} is required and must be a string")
        if len(name) > 50:
            raise ValueError(f"{field_name} must not exceed 50 characters")
        return name
    
    def _validate_email(self, email):
        """
        Validate email format
        
        Args:
            email (str): Email to validate
            
        Returns:
            str: Validated email
            
        Raises:
            ValueError: If email is invalid
        """
        if not email or not isinstance(email, str):
            raise ValueError("Email is required and must be a string")
        
        # Basic email validation
        if '@' not in email or '.' not in email.split('@')[1]:
            raise ValueError("Invalid email format")
        
        return email
