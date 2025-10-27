"""
Amenity API endpoints for the HBnB application.
This module handles CRUD operations (Create, Read, Update) for amenities.
"""

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    """Handles operations on the amenity collection"""
    
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new amenity"""
        try:
            
            amenity_data = api.payload
            
            new_amenity = facade.create_amenity(amenity_data)
            
            result = new_amenity.to_dict()
            
            return result, 201
            
        except ValueError as e:
            return {'error': str(e)}, 400
            
        except Exception as e:
            return {'error': 'An error occurred while creating the amenity'}, 500

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        try:
            # Get all amenities using the facade
            amenities = facade.get_all_amenities()
            
            # Return list of amenities with their details
            return [
                {
                    'id': amenity.id,
                    'name': amenity.name
                }
                for amenity in amenities
            ], 200
            
        except Exception as e:
            return {'error': 'An error occurred while retrieving amenities'}, 500


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    """Handles operations on a single amenity"""
    
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            # Retrieve the amenity by ID using the facade
            amenity = facade.get_amenity(amenity_id)
            
            return {
                'id': amenity.id,
                'name': amenity.name
            }, 200
            
        except ValueError as e:
            return {'error': 'Amenity not found'}, 404
        except Exception as e:
            return {'error': 'An error occurred while retrieving the amenity'}, 500

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload
        
        # Validate input data
        if not amenity_data or 'name' not in amenity_data:
            return {'error': 'Invalid input data'}, 400
        
        # Check if name is empty or only whitespace
        if not amenity_data['name'].strip():
            return {'error': 'Amenity name cannot be empty'}, 400
        
        try:
            # Update the amenity using the facade
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            
            return {
                'message': 'Amenity updated successfully'
            }, 200
            
        except ValueError as e:
            error_message = str(e)
            if 'not found' in error_message.lower():
                return {'error': 'Amenity not found'}, 404
            return {'error': error_message}, 400
        except Exception as e:
            return {'error': 'An error occurred while updating the amenity'}, 500
