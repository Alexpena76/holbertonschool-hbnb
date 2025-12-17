"""
User model for authentication and user management
"""

from app import db, bcrypt  # SQLALCHEMY MAPPING: Import db and bcrypt
from app.models.base_model import BaseModel
import re


# SQLALCHEMY MAPPING: User now inherits from BaseModel (which is a db.Model)
class User(BaseModel):
    """
    User entity representing application users.
    
    Attributes:
        first_name (str): User's first name
        last_name (str): User's last name
        email (str): User's email (unique)
        password (str): User's hashed password
        is_admin (bool): Whether user has admin privileges
    
    Relationships:
        places: One-to-Many with Place (user owns many places)
        reviews: One-to-Many with Review (user writes many reviews)
    
    SQLALCHEMY MAPPING: This class is now a SQLAlchemy model that maps
    to the 'users' table in the database.
    """
    
    # SQLALCHEMY MAPPING: Define the table name
    __tablename__ = 'users'
    
    # SQLALCHEMY MAPPING: Define database columns with constraints
    first_name = db.Column(
        db.String(50),  # Maximum length 50 characters
        nullable=False  # Cannot be NULL
    )
    
    last_name = db.Column(
        db.String(50),  # Maximum length 50 characters
        nullable=False  # Cannot be NULL
    )
    
    email = db.Column(
        db.String(120),  # Maximum length 120 characters
        nullable=False,  # Cannot be NULL
        unique=True  # Must be unique across all users
    )
    
    password = db.Column(
        db.String(128),  # Hashed password length
        nullable=False  # Cannot be NULL
    )
    
    is_admin = db.Column(
        db.Boolean,  # True or False
        default=False  # Default is not admin
    )
    
    # ==================== RELATIONSHIPS ====================
    
    # RELATIONSHIP: One-to-Many with Place
    # One user can own many places
    places = db.relationship(
        'Place',  # The related model name
        backref='owner',  # Creates reverse reference: place.owner -> User
        lazy=True,  # Load places when accessed (not automatically)
        cascade='all, delete-orphan'  # If user is deleted, delete all their places
    )
    # Usage examples:
    #   user.places -> list of all places owned by this user
    #   place.owner -> the user who owns this place
    
    # RELATIONSHIP: One-to-Many with Review
    # One user can write many reviews
    reviews = db.relationship(
        'Review',  # The related model name
        backref='user',  # Creates reverse reference: review.user -> User
        lazy=True,  # Load reviews when accessed (not automatically)
        cascade='all, delete-orphan'  # If user is deleted, delete all their reviews
    )
    # Usage examples:
    #   user.reviews -> list of all reviews written by this user
    #   review.user -> the user who wrote this review
    
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """
        Initialize a User instance
        
        Args:
            first_name (str): User's first name
            last_name (str): User's last name
            email (str): User's email
            password (str): User's plain text password (will be hashed)
            is_admin (bool): Whether user is an admin (default: False)
        
        SQLALCHEMY MAPPING: SQLAlchemy will automatically set id, created_at,
        and updated_at when this object is added to the database.
        
        RELATIONSHIPS: The places and reviews relationships are automatically
        initialized as empty lists by SQLAlchemy.
        """
        # Validate and set attributes
        self.first_name = self._validate_name(first_name, "First name")
        self.last_name = self._validate_name(last_name, "Last name")
        self.email = self._validate_email(email)
        self.is_admin = is_admin
        
        # Hash the password before storing
        self.hash_password(password)
    
    def _validate_name(self, name, field_name):
        """
        Validate name fields (first_name, last_name)
        
        Args:
            name (str): Name to validate
            field_name (str): Field name for error messages
            
        Returns:
            str: Validated and cleaned name
            
        Raises:
            ValueError: If validation fails
        """
        if not name or not isinstance(name, str):
            raise ValueError(f"{field_name} is required and must be a string")
        
        name = name.strip()
        
        if len(name) == 0:
            raise ValueError(f"{field_name} cannot be empty")
        
        if len(name) > 50:
            raise ValueError(f"{field_name} must be less than 50 characters")
        
        return name
    
    def _validate_email(self, email):
        """
        Validate email format
        
        Args:
            email (str): Email to validate
            
        Returns:
            str: Validated and cleaned email (lowercase)
            
        Raises:
            ValueError: If email format is invalid
        """
        if not email or not isinstance(email, str):
            raise ValueError("Email is required and must be a string")
        
        email = email.strip().lower()
        
        # Basic email regex pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")
        
        return email
    
    def hash_password(self, password):
        """
        Hash the password before storing it
        
        Args:
            password (str): Plain text password
            
        Raises:
            ValueError: If password is invalid
        
        SQLALCHEMY MAPPING: The hashed password is stored in the
        password column in the database.
        """
        if not password or not isinstance(password, str):
            raise ValueError("Password is required and must be a string")
        
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        
        # Hash the password using bcrypt
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password):
        """
        Verify a password against the hashed password
        
        Args:
            password (str): Plain text password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return bcrypt.check_password_hash(self.password, password)
    
    def to_dict(self):
        """
        Convert user instance to dictionary (excludes password)
        
        Returns:
            dict: User data without sensitive information
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