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

