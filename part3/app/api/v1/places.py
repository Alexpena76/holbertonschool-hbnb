"""
Place API endpoints
Handles CRUD operations for places through RESTful API
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt  # ADMIN ADDITION: Added get_jwt
from app.services import facade

# Create namespace for place operations
api = Namespace('places', description='Place operations')

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(required=True, description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner')
})


@api.route('/')
class PlaceList(Resource):
    """
    Handles operations on the place collection
    - GET: Retrieve list of all places (PUBLIC)
    - POST: Create a new place (AUTHENTICATED)
    """
    
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """
        Retrieve a list of all places (PUBLIC - No authentication required)
        
        Returns:
            list: List of place dictionaries with status 200
            
        Example Response:
            [
                {
                    "id": "uuid-1",
                    "title": "Beach House",
                    "description": "Beautiful beach house",
                    "price": 150.0,
                    "latitude": 34.0522,
                    "longitude": -118.2437,
                    "owner_id": "owner-uuid"
                },
                ...
            ]
        """
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200
    
    @jwt_required()  # JWT AUTHENTICATION: Requires valid token
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized - Invalid or missing token')
    def post(self):
        """
        Create a new place (AUTHENTICATED - Requires JWT token)
        
        The authenticated user becomes the owner of the place.
        The owner_id is automatically set from the JWT token.
        
        Returns:
            dict: Created place data with status 201
            dict: Error message with status 400 if validation fails
            
        Example Request:
            Headers:
                Authorization: Bearer <jwt_token>
            Body:
                {
                    "title": "Beach House",
                    "description": "Beautiful beach house",
                    "price": 150.0,
                    "latitude": 34.0522,
                    "longitude": -118.2437,
                    "owner_id": "will-be-overwritten"
                }
                
        Example Success Response:
            {
                "id": "uuid",
                "title": "Beach House",
                "description": "Beautiful beach house",
                "price": 150.0,
                "latitude": 34.0522,
                "longitude": -118.2437,
                "owner_id": "authenticated-user-uuid"
            }
        """
        # JWT AUTHENTICATION: Get the current user's ID from the JWT token
        current_user = get_jwt_identity()
        
        place_data = api.payload
        
        # OWNERSHIP VALIDATION: Set owner_id to the authenticated user
        place_data['owner_id'] = current_user
        
        try:
            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<place_id>')
@api.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    """
    Handles operations on individual places
    - GET: Retrieve place details (PUBLIC)
    - PUT: Update place information (AUTHENTICATED - Owner or ADMIN)
    """
    
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Get place details by ID (PUBLIC - No authentication required)
        
        Args:
            place_id (str): Place's unique identifier
            
        Returns:
            dict: Place data with status 200 if found
            dict: Error message with status 404 if not found
            
        Example Response:
            {
                "id": "uuid",
                "title": "Beach House",
                "description": "Beautiful beach house",
                "price": 150.0,
                "latitude": 34.0522,
                "longitude": -118.2437,
                "owner_id": "owner-uuid"
            }
        """
        place = facade.get_place(place_id)
        
        if not place:
            return {'error': 'Place not found'}, 404
        
        return place.to_dict(), 200
    
    @jwt_required()  # JWT AUTHENTICATION: Requires valid token
    @api.expect(place_model)
    @api.response(200, 'Place successfully updated')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized - Invalid or missing token')
    def put(self, place_id):
        """
        Update place information (AUTHENTICATED - Owner or ADMIN)
        
        Only the owner of the place can modify its information,
        UNLESS the user is an administrator.
        
        ADMIN ADDITION: Administrators can now modify ANY place,
        bypassing the ownership restriction that applies to regular users.
        
        Args:
            place_id (str): Place's unique identifier
            
        Returns:
            dict: Updated place data with status 200
            dict: Error message with status 403 if not owner (and not admin)
            dict: Error message with status 404 if place not found
            
        Example Request:
            Headers:
                Authorization: Bearer <jwt_token>
            Body:
                {
                    "title": "Updated Beach House",
                    "description": "Even more beautiful",
                    "price": 200.0
                }
                
        Example Success Response:
            {
                "id": "uuid",
                "title": "Updated Beach House",
                "description": "Even more beautiful",
                "price": 200.0,
                "latitude": 34.0522,
                "longitude": -118.2437,
                "owner_id": "owner-uuid"
            }
            
        Example Error Response (Non-Owner):
            {
                "error": "Unauthorized action"
            }
        """
        # JWT AUTHENTICATION: Get the current user's ID from the JWT token
        current_user = get_jwt_identity()
        
        # ADMIN ADDITION: Get admin status from JWT claims
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        place = facade.get_place(place_id)
        
        if not place:
            return {'error': 'Place not found'}, 404
        
        # ADMIN ADDITION: Ownership validation with admin bypass
        # Admins can modify any place, regular users only their own
        if not is_admin and str(place.owner_id) != current_user:
            return {'error': 'Unauthorized action'}, 403
        
        place_data = api.payload
        
        # Security: Prevent changing the owner_id
        if 'owner_id' in place_data:
            del place_data['owner_id']
        
        try:
            updated_place = facade.update_place(place_id, place_data)
            return updated_place.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400