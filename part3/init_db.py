"""
Database initialization script
Run this to create all database tables
"""

from app import create_app, db
from app.models.user import User  # SQLALCHEMY MAPPING: Import all models
from app.models.amenity import Amenity  # SQLALCHEMY MAPPING: Import Amenity model
from app.models.place import Place  # SQLALCHEMY MAPPING: Import Place model
from app.models.review import Review  # SQLALCHEMY MAPPING: Import Review model
from app.models import place_amenity  # RELATIONSHIPS: Import association table


def init_database():
    """
    Initialize the database and create all tables
    
    SQLALCHEMY MAPPING: This creates all tables in the database
    based on the User, Amenity, Place, and Review model definitions.
    
    RELATIONSHIPS: Also creates the place_amenity association table
    for the many-to-many relationship between Place and Amenity.
    """
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        
        # SQLALCHEMY MAPPING: Create all tables defined by models
        db.create_all()
        
        print("✓ Database tables created successfully!")
        print("\nTables created:")
        print("  - users (from User model)")
        print("  - amenities (from Amenity model)")
        print("  - places (from Place model)")
        print("  - reviews (from Review model)")
        print("  - place_amenity (association table for Place-Amenity many-to-many)")  # RELATIONSHIPS: Association table
        
        # Check if tables were created
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        print("\n" + "="*60)
        print("VERIFICATION - Tables in database:")
        print("="*60)
        
        # SQLALCHEMY MAPPING: Verify users table
        if 'users' in tables:
            print("\n✓ 'users' table exists")
            
            # Show column information
            columns = inspector.get_columns('users')
            print("  Columns:")
            for column in columns:
                nullable = "NULL" if column['nullable'] else "NOT NULL"
                print(f"    - {column['name']}: {column['type']} ({nullable})")
            
            # RELATIONSHIPS: Show foreign keys (none for users)
            foreign_keys = inspector.get_foreign_keys('users')
            if foreign_keys:
                print("  Foreign Keys:")
                for fk in foreign_keys:
                    print(f"    - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
        else:
            print("\n✗ Warning: 'users' table not found!")
        
        # SQLALCHEMY MAPPING: Verify amenities table
        if 'amenities' in tables:
            print("\n✓ 'amenities' table exists")
            
            # Show column information
            columns = inspector.get_columns('amenities')
            print("  Columns:")
            for column in columns:
                nullable = "NULL" if column['nullable'] else "NOT NULL"
                print(f"    - {column['name']}: {column['type']} ({nullable})")
            
            # RELATIONSHIPS: Show foreign keys (none for amenities)
            foreign_keys = inspector.get_foreign_keys('amenities')
            if foreign_keys:
                print("  Foreign Keys:")
                for fk in foreign_keys:
                    print(f"    - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
        else:
            print("\n✗ Warning: 'amenities' table not found!")
        
        # SQLALCHEMY MAPPING: Verify places table
        if 'places' in tables:
            print("\n✓ 'places' table exists")
            
            # Show column information
            columns = inspector.get_columns('places')
            print("  Columns:")
            for column in columns:
                nullable = "NULL" if column['nullable'] else "NOT NULL"
                print(f"    - {column['name']}: {column['type']} ({nullable})")
            
            # RELATIONSHIPS: Show foreign keys
            foreign_keys = inspector.get_foreign_keys('places')
            if foreign_keys:
                print("  Foreign Keys:")
                for fk in foreign_keys:
                    print(f"    - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
        else:
            print("\n✗ Warning: 'places' table not found!")
        
        # SQLALCHEMY MAPPING: Verify reviews table
        if 'reviews' in tables:
            print("\n✓ 'reviews' table exists")
            
            # Show column information
            columns = inspector.get_columns('reviews')
            print("  Columns:")
            for column in columns:
                nullable = "NULL" if column['nullable'] else "NOT NULL"
                print(f"    - {column['name']}: {column['type']} ({nullable})")
            
            # RELATIONSHIPS: Show foreign keys
            foreign_keys = inspector.get_foreign_keys('reviews')
            if foreign_keys:
                print("  Foreign Keys:")
                for fk in foreign_keys:
                    print(f"    - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
        else:
            print("\n✗ Warning: 'reviews' table not found!")
        
        # RELATIONSHIPS: Verify place_amenity association table
        if 'place_amenity' in tables:
            print("\n✓ 'place_amenity' association table exists")
            
            # Show column information
            columns = inspector.get_columns('place_amenity')
            print("  Columns:")
            for column in columns:
                nullable = "NULL" if column['nullable'] else "NOT NULL"
                print(f"    - {column['name']}: {column['type']} ({nullable})")
            
            # RELATIONSHIPS: Show foreign keys (should have 2)
            foreign_keys = inspector.get_foreign_keys('place_amenity')
            if foreign_keys:
                print("  Foreign Keys:")
                for fk in foreign_keys:
                    print(f"    - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
        else:
            print("\n✗ Warning: 'place_amenity' table not found!")
        
        print("\n" + "="*60)
        print("Database initialization complete!")
        print("="*60)


if __name__ == '__main__':
    init_database()