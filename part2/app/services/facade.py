# ==================== FILE: app/services/facade.py ====================
"""
Facade Pattern Implementation - UPDATED
Provides a unified interface to coordinate operations across
business logic and persistence layers
"""

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    """
    Facade class that coordinates all business operations
    """
    
    def __init__(self):
        """Initialize facade with repository instances"""
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ==================== USER METHODS ====================
    
    def create_user(self, user_data):
        """
        Create a new user
        
        Args:
            user_data (dict): Dictionary containing user information
                - first_name (str): User's first name
                - last_name (str): User's last name
                - email (str): User's email address
                - is_admin (bool, optional): Admin flag
        
        Returns:
            User: Created user object
            
        Raises:
            ValueError: If validation fails
        """
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """
        Retrieve a user by ID
        
        Args:
            user_id (str): User's unique identifier
            
        Returns:
            User: User object if found, None otherwise
        """
        return self.user_repo.get(user_id)
    
    def get_all_users(self):
        """
        Retrieve all users
        
        Returns:
            list: List of all User objects
        """
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        """
        Find a user by email address
        
        Args:
            email (str): Email address to search for
            
        Returns:
            User: User object if found, None otherwise
        """
        return self.user_repo.get_by_attribute('email', email)
    
    def update_user(self, user_id, user_data):
        """
        Update user information
        
        Args:
            user_id (str): User's unique identifier
            user_data (dict): Dictionary containing fields to update
            
        Returns:
            User: Updated user object if found, None otherwise
        """
        user = self.user_repo.get(user_id)
        if user:
            # Validate email uniqueness if email is being updated
            if 'email' in user_data and user_data['email'] != user.email:
                existing_user = self.get_user_by_email(user_data['email'])
                if existing_user and existing_user.id != user_id:
                    raise ValueError("Email already registered")
            
            self.user_repo.update(user_id, user_data)
            return user
        return None

    # ==================== PLACE METHODS (Placeholders) ====================
    
"""
Place API endpoints for the HBnB application.
This module handles CRUD operations (Create, Read, Update) for places,
including relationships with users (owners) and amenities.
"""

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})


@api.route('/')
class PlaceList(Resource):
    """Handles operations on the place collection"""
    
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        
        # Validate required fields
        required_fields = ['title', 'price', 'latitude', 'longitude', 'owner_id']
        for field in required_fields:
            if field not in place_data:
                return {'error': f'{field} is required'}, 400
        
        # Validate title is not empty
        if not place_data['title'].strip():
            return {'error': 'Title cannot be empty'}, 400
        
        try:
            # Create the place using the facade
            new_place = facade.create_place(place_data)
            
            # Prepare response with place details
            response = {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner_id
            }
            
            # Include amenities if available
            if hasattr(new_place, 'amenities') and new_place.amenities:
                response['amenities'] = [
                    {'id': amenity.id, 'name': amenity.name}
                    for amenity in new_place.amenities
                ]
            
            return response, 201
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'An error occurred while creating the place'}, 500

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        try:
            # Get all places using the facade
            places = facade.get_all_places()
            
            # Return simplified list of places
            return [
                {
                    'id': place.id,
                    'title': place.title,
                    'latitude': place.latitude,
                    'longitude': place.longitude
                }
                for place in places
            ], 200
            
        except Exception as e:
            return {'error': 'An error occurred while retrieving places'}, 500


@api.route('/<place_id>')
class PlaceResource(Resource):
    """Handles operations on a single place"""
    
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        try:
            # Retrieve the place by ID using the facade
            place = facade.get_place(place_id)
            
            # Prepare detailed response
            response = {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'price': place.price
            }
            
            # Include owner information
            if hasattr(place, 'owner') and place.owner:
                response['owner'] = {
                    'id': place.owner.id,
                    'first_name': place.owner.first_name,
                    'last_name': place.owner.last_name,
                    'email': place.owner.email
                }
            else:
                # Fallback: fetch owner separately if not loaded
                owner = facade.get_user(place.owner_id)
                if owner:
                    response['owner'] = {
                        'id': owner.id,
                        'first_name': owner.first_name,
                        'last_name': owner.last_name,
                        'email': owner.email
                    }
            
            # Include amenities information
            if hasattr(place, 'amenities') and place.amenities:
                response['amenities'] = [
                    {
                        'id': amenity.id,
                        'name': amenity.name
                    }
                    for amenity in place.amenities
                ]
            else:
                response['amenities'] = []
            
            return response, 200
            
        except ValueError as e:
            return {'error': 'Place not found'}, 404
        except Exception as e:
            return {'error': 'An error occurred while retrieving the place'}, 500

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        
        # Validate that at least one field is provided for update
        if not place_data:
            return {'error': 'No data provided for update'}, 400
        
        # Validate title if provided
        if 'title' in place_data and not place_data['title'].strip():
            return {'error': 'Title cannot be empty'}, 400
        
        try:
            # Update the place using the facade
            updated_place = facade.update_place(place_id, place_data)
            
            return {
                'message': 'Place updated successfully'
            }, 200
            
        except ValueError as e:
            error_message = str(e)
            if 'not found' in error_message.lower():
                return {'error': 'Place not found'}, 404
            return {'error': error_message}, 400
        except Exception as e:
            return {'error': 'An error occurred while updating the place'}, 500

    # ==================== REVIEW METHODS (Placeholders) ====================
    
    def create_review(self, review_data):
        """Create a new review (to be implemented)"""
        pass
    
    def get_review(self, review_id):
        """Retrieve a review by ID (to be implemented)"""
        pass
    
    def get_all_reviews(self):
        """Retrieve all reviews (to be implemented)"""
        pass
    
    def update_review(self, review_id, review_data):
        """Update review information (to be implemented)"""
        pass

    # ==================== AMENITY METHODS ====================
    def create_amenity(self, amenity_data):
        """
        Create a new amenity
        
        Args:
            amenity_data (dict): Dictionary containing amenity information
            
        Returns:
            Amenity: The newly created amenity object
            
        Raises:
            ValueError: If the amenity data is invalid or amenity name already exists
        """
        
        # Validate that name is provided
        if 'name' not in amenity_data or not amenity_data['name']:
            raise ValueError("Amenity name is required")
        
        # Validate that name is not empty or just whitespace
        if not amenity_data['name'].strip():
            raise ValueError("Amenity name cannot be empty")
        
        # Check if amenity with the same name already exists
        existing_amenities = self.amenity_repo.get_all()
        for amenity in existing_amenities:
            if amenity.name.lower() == amenity_data['name'].strip().lower():
                raise ValueError("Amenity with this name already exists")
        
        # Create the new amenity
        new_amenity = Amenity(name=amenity_data['name'].strip())
        
        # Save to repository
        self.amenity_repo.add(new_amenity)
        
        return new_amenity


    def get_amenity(self, amenity_id):
        """
        Retrieve an amenity by ID
        
        Args:
            amenity_id (str): The UUID of the amenity
            
        Returns:
            Amenity: The amenity object if found, None otherwise
            
        Raises:
            ValueError: If the amenity is not found
        """
        # Retrieve the amenity from the repository
        amenity = self.amenity_repo.get(amenity_id)
        
        if not amenity:
            raise ValueError(f"Amenity with ID {amenity_id} not found")
        
        return amenity


    def get_all_amenities(self):
        """
        Retrieve all amenities
        
        Returns:
            list: List of all amenity objects
        """
        # Get all amenities from the repository
        return self.amenity_repo.get_all()


    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an existing amenity
        
        Args:
            amenity_id (str): The UUID of the amenity to update
            amenity_data (dict): Dictionary containing updated amenity information
            
        Returns:
            Amenity: The updated amenity object
            
        Raises:
            ValueError: If the amenity is not found or data is invalid
        """
        # Validate that name is provided
        if 'name' not in amenity_data or not amenity_data['name']:
            raise ValueError("Amenity name is required")
        
        # Validate that name is not empty or just whitespace
        if not amenity_data['name'].strip():
            raise ValueError("Amenity name cannot be empty")
        
        # Retrieve the existing amenity
        amenity = self.amenity_repo.get(amenity_id)
        
        if not amenity:
            raise ValueError(f"Amenity with ID {amenity_id} not found")
        
        # Check if another amenity with the same name already exists (excluding current amenity)
        existing_amenities = self.amenity_repo.get_all()
        for existing_amenity in existing_amenities:
            if (existing_amenity.id != amenity_id and 
                existing_amenity.name.lower() == amenity_data['name'].strip().lower()):
                raise ValueError("Amenity with this name already exists")
        
        # Update the amenity's name
        amenity.name = amenity_data['name'].strip()
        
        # Save the updated amenity to the repository
        self.amenity_repo.update(amenity_id, amenity_data)
        
        return amenity
