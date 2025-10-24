"""
Places API endpoints
Handles CRUD operations for places
"""

from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')

# Initialize facade
facade = HBnBFacade()

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude coordinate'),
    'longitude': fields.Float(required=True, description='Longitude coordinate'),
    'owner_id': fields.String(required=True, description='ID of the place owner')
})


@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    def get(self):
        """List all places"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200

    @api.expect(place_model)
    @api.doc('create_place')
    def post(self):
        """Create a new place"""
        try:
            place_data = api.payload
            
            # Validate required fields
            required_fields = ['title', 'price', 'latitude', 'longitude', 'owner_id']
            for field in required_fields:
                if field not in place_data:
                    return {'error': f'{field} is required'}, 400
            
            # Verify owner exists
            owner = facade.get_user(place_data['owner_id'])
            if not owner:
                return {'error': 'Owner not found'}, 400
            
            # Create the place
            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'An error occurred while creating the place'}, 500


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.doc('get_place')
    def get(self, place_id):
        """Get a place by ID"""
        try:
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404
            
            # Build response with place details
            response = place.to_dict()
            
            # Include amenities information if available
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
            
        except Exception as e:
            return {'error': 'Place not found'}, 404

    @api.expect(place_model)
    @api.doc('update_place')
    def put(self, place_id):
        """Update a place"""
        try:
            place_data = api.payload
            
            # Verify place exists
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404
            
            # If owner_id is being updated, verify new owner exists
            if 'owner_id' in place_data:
                owner = facade.get_user(place_data['owner_id'])
                if not owner:
                    return {'error': 'Owner not found'}, 400
            
            # Update the place
            updated_place = facade.update_place(place_id, place_data)
            return updated_place.to_dict(), 200
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'An error occurred while updating the place'}, 500
