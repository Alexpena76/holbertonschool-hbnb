"""
Models package initialization
Defines association tables and imports all models
"""

from app import db

# MANY-TO-MANY RELATIONSHIP: Association table for Place <-> Amenity
# This table manages the many-to-many relationship between places and amenities
place_amenity = db.Table(
    'place_amenity',  # Table name
    db.Column(
        'place_id',
        db.String(36),
        db.ForeignKey('places.id'),  # Foreign key to places table
        primary_key=True  # Part of composite primary key
    ),
    db.Column(
        'amenity_id',
        db.String(36),
        db.ForeignKey('amenities.id'),  # Foreign key to amenities table
        primary_key=True  # Part of composite primary key
    )
)

# Import all models so SQLAlchemy knows about them
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

# Export models for easy importing
__all__ = ['User', 'Place', 'Review', 'Amenity', 'place_amenity']