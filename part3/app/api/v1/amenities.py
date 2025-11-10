"""
Amenity API endpoints
Handles CRUD operations for amenities through RESTful API
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt  # ADMIN ADDITION: Added JWT imports
from app.services import facade

# Create namespace for amenity operations
api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    """
    Handles operations on the amenity collection
    - GET: Retrieve list of all amenities (PUBLIC)
    - POST: Create a new amenity (ADMIN ONLY)  # ADMIN ADDITION: Now requires admin
    """
    
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """
        Retrieve a list of all amenities (PUBLIC)
        
        Returns:
            list: List of amenity dictionaries with status 200
        """
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200
    
    @jwt_required()  # ADMIN ADDITION: Requires authentication
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data or amenity already exists')
    @api.response(403, 'Admin privileges required')  # ADMIN ADDITION: New error response
    def post(self):
        """
        Create a new amenity (ADMIN ONLY)
        
        ADMIN ADDITION: This endpoint is now restricted to administrators only.
        Only admins can create new amenities in the system.
        
        Returns:
            dict: Created amenity data with status 201
            dict: Error message with status 403 if not admin
        """
        # ADMIN ADDITION: Check if user is admin
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        if not is_admin:
            return {'error': 'Admin privileges required'}, 403
        
        amenity_data = api.payload
        
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    """
    Handles operations on individual amenities
    - GET: Retrieve amenity details (PUBLIC)
    - PUT: Update amenity information (ADMIN ONLY)  # ADMIN ADDITION: Now requires admin
    """
    
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """
        Get amenity details by ID (PUBLIC)
        
        Args:
            amenity_id (str): Amenity's unique identifier
            
        Returns:
            dict: Amenity data with status 200 if found
        """
        amenity = facade.get_amenity(amenity_id)
        
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        return amenity.to_dict(), 200
    
    @jwt_required()  # ADMIN ADDITION: Requires authentication
    @api.expect(amenity_model)
    @api.response(200, 'Amenity successfully updated')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')  # ADMIN ADDITION: New error response
    def put(self, amenity_id):
        """
        Update amenity information (ADMIN ONLY)
        
        ADMIN ADDITION: This endpoint is now restricted to administrators only.
        Only admins can modify existing amenities.
        
        Args:
            amenity_id (str): Amenity's unique identifier
            
        Returns:
            dict: Updated amenity data with status 200
            dict: Error message with status 403 if not admin
        """
        # ADMIN ADDITION: Check if user is admin
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        if not is_admin:
            return {'error': 'Admin privileges required'}, 403
        
        amenity_data = api.payload
        
        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            
            if not updated_amenity:
                return {'error': 'Amenity not found'}, 404
            
            return updated_amenity.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400