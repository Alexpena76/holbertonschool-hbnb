"""
User Model
Represents a user in the HBnB application
"""

from app.models.base_model import BaseModel
import re


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
            str: Validated and cleaned name
            
        Raises:
            ValueError: If name is invalid
        """
        # Check if name exists and is a string
        if not name or not isinstance(name, str):
            raise ValueError(f"{field_name} is required and must be a string")
        
        # Check if name is not just whitespace
        if not name.strip():
            raise ValueError(f"{field_name} cannot be empty or just whitespace")
        
        # Check length
        if len(name.strip()) > 50:
            raise ValueError(f"{field_name} must not exceed 50 characters")
        
        return name.strip()
    
    def _validate_email(self, email):
        """
        Validate email format
        
        Args:
            email (str): Email to validate
            
        Returns:
            str: Validated and cleaned email (lowercase)
            
        Raises:
            ValueError: If email is invalid
        """
        # Check if email exists and is a string
        if not email or not isinstance(email, str):
            raise ValueError("Email is required and must be a string")
        
        # Check if email is not just whitespace
        if not email.strip():
            raise ValueError("Email cannot be empty or just whitespace")
        
        # Validate email format using regex
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email.strip()):
            raise ValueError("Invalid email format")
        
        return email.strip().lower()
    
    def to_dict(self):
        """
        Convert user to dictionary representation
        
        Returns:
            dict: User data as dictionary
        """
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }