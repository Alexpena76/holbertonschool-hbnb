"""
Configuration classes for the HBnB application.
"""

import os
from datetime import timedelta


class Config:
    """
    Base configuration class.
    Contains settings common to all environments.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    DEBUG = False
    TESTING = False
    
    # JWT configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # SQLALCHEMY ADDITION: Database configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking to save memory


class DevelopmentConfig(Config):
    """
    Development environment configuration.
    """
    DEBUG = True
    
    # JWT configuration for development
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # SQLALCHEMY ADDITION: Development database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'  # SQLite database for development


class TestingConfig(Config):
    """
    Testing environment configuration.
    """
    TESTING = True
    
    # JWT configuration for testing
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    
    # SQLALCHEMY ADDITION: Testing database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'  # Separate database for testing


class ProductionConfig(Config):
    """
    Production environment configuration.
    """
    DEBUG = False
    
    # JWT configuration for production
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # SQLALCHEMY ADDITION: Production database configuration
    # In production, use environment variable for database URI
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///production.db'  # Fallback to SQLite if DATABASE_URL not set
    )
    
    # Additional production settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'