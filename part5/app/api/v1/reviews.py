"""
Review API endpoints
Handles CRUD operations for reviews through RESTful API
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt  # ADMIN ADDITION: Added get_jwt
from app.services import facade

# Create namespace for review operations
api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    """
    Handles operations on the review collection
    - GET: Retrieve list of all reviews (PUBLIC)
    - POST: Create a new review (AUTHENTICATED)
    """
    
    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """
        Retrieve a list of all reviews (PUBLIC - No authentication required)
        
        Returns:
            list: List of review dictionaries with status 200
            
        Example Response:
            [
                {
                    "id": "uuid-1",
                    "text": "Great place!",
                    "rating": 5,
                    "user_id": "user-uuid",
                    "place_id": "place-uuid"
                },
                ...
            ]
        """
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200
    
    @jwt_required()  # JWT AUTHENTICATION: Requires valid token
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data or validation error')
    @api.response(401, 'Unauthorized - Invalid or missing token')
    @api.response(404, 'Place not found')
    def post(self):
        """
        Create a new review (AUTHENTICATED - Requires JWT token)
        
        Validation Rules:
        - Users cannot review their own places
        - Users can only review a place once
        
        Returns:
            dict: Created review data with status 201
            dict: Error message with status 400 if validation fails
            
        Example Request:
            Headers:
                Authorization: Bearer <jwt_token>
            Body:
                {
                    "text": "Amazing place!",
                    "rating": 5,
                    "place_id": "place-uuid",
                    "user_id": "will-be-overwritten"
                }
                
        Example Success Response:
            {
                "id": "uuid",
                "text": "Amazing place!",
                "rating": 5,
                "user_id": "authenticated-user-uuid",
                "place_id": "place-uuid"
            }
            
        Example Error Responses:
            {"error": "You cannot review your own place"} - 400
            {"error": "You have already reviewed this place"} - 400
        """
        # JWT AUTHENTICATION: Get the current user's ID from the JWT token
        current_user = get_jwt_identity()
        
        review_data = api.payload
        place_id = review_data.get('place_id')
        
        # Validate that the place exists
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        # VALIDATION 1: Users cannot review their own places
        if str(place.owner_id) == current_user:
            return {'error': 'You cannot review your own place'}, 400
        
        # VALIDATION 2: Check if user has already reviewed this place
        existing_reviews = facade.get_reviews_by_place(place_id)
        for review in existing_reviews:
            if str(review.user_id) == current_user:
                return {'error': 'You have already reviewed this place'}, 400
        
        # Override user_id with authenticated user's ID for security
        review_data['user_id'] = current_user
        
        try:
            new_review = facade.create_review(review_data)
            return new_review.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<review_id>')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    """
    Handles operations on individual reviews
    - GET: Retrieve review details (PUBLIC)
    - PUT: Update review information (AUTHENTICATED - Author or ADMIN)
    - DELETE: Delete review (AUTHENTICATED - Author or ADMIN)
    """
    
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """
        Get review details by ID (PUBLIC - No authentication required)
        
        Args:
            review_id (str): Review's unique identifier
            
        Returns:
            dict: Review data with status 200 if found
            dict: Error message with status 404 if not found
            
        Example Response:
            {
                "id": "uuid",
                "text": "Great place!",
                "rating": 5,
                "user_id": "user-uuid",
                "place_id": "place-uuid"
            }
        """
        review = facade.get_review(review_id)
        
        if not review:
            return {'error': 'Review not found'}, 404
        
        return review.to_dict(), 200
    
    @jwt_required()  # JWT AUTHENTICATION: Requires valid token
    @api.expect(review_model)
    @api.response(200, 'Review successfully updated')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized - Invalid or missing token')
    def put(self, review_id):
        """
        Update review information (AUTHENTICATED - Author or ADMIN)
        
        Only the author of the review can modify it,
        UNLESS the user is an administrator.
        
        ADMIN ADDITION: Administrators can now modify ANY review,
        bypassing the authorship restriction that applies to regular users.
        
        Args:
            review_id (str): Review's unique identifier
            
        Returns:
            dict: Updated review data with status 200
            dict: Error message with status 403 if not author (and not admin)
            dict: Error message with status 404 if review not found
            
        Example Request:
            Headers:
                Authorization: Bearer <jwt_token>
            Body:
                {
                    "text": "Updated review text",
                    "rating": 4
                }
                
        Example Success Response:
            {
                "id": "uuid",
                "text": "Updated review text",
                "rating": 4,
                "user_id": "user-uuid",
                "place_id": "place-uuid"
            }
            
        Example Error Response (Non-Author):
            {
                "error": "Unauthorized action"
            }
        """
        # JWT AUTHENTICATION: Get the current user's ID from the JWT token
        current_user = get_jwt_identity()
        
        # ADMIN ADDITION: Get admin status from JWT claims
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        review = facade.get_review(review_id)
        
        if not review:
            return {'error': 'Review not found'}, 404
        
        # ADMIN ADDITION: Ownership validation with admin bypass
        # Admins can modify any review, regular users only their own
        if not is_admin and str(review.user_id) != current_user:
            return {'error': 'Unauthorized action'}, 403
        
        review_data = api.payload
        
        # Security: Prevent changing user_id and place_id
        if 'user_id' in review_data:
            del review_data['user_id']
        if 'place_id' in review_data:
            del review_data['place_id']
        
        try:
            updated_review = facade.update_review(review_id, review_data)
            return updated_review.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
    
    @jwt_required()  # JWT AUTHENTICATION: Requires valid token
    @api.response(200, 'Review successfully deleted')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @api.response(401, 'Unauthorized - Invalid or missing token')
    def delete(self, review_id):
        """
        Delete a review (AUTHENTICATED - Author or ADMIN)
        
        Only the author of the review can delete it,
        UNLESS the user is an administrator.
        
        ADMIN ADDITION: Administrators can now delete ANY review,
        bypassing the authorship restriction that applies to regular users.
        
        Args:
            review_id (str): Review's unique identifier
            
        Returns:
            dict: Success message with status 200
            dict: Error message with status 403 if not author (and not admin)
            dict: Error message with status 404 if review not found
            
        Example Request:
            Headers:
                Authorization: Bearer <jwt_token>
                
        Example Success Response:
            {
                "message": "Review deleted successfully"
            }
            
        Example Error Response (Non-Author):
            {
                "error": "Unauthorized action"
            }
        """
        # JWT AUTHENTICATION: Get the current user's ID from the JWT token
        current_user = get_jwt_identity()
        
        # ADMIN ADDITION: Get admin status from JWT claims
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        review = facade.get_review(review_id)
        
        if not review:
            return {'error': 'Review not found'}, 404
        
        # ADMIN ADDITION: Ownership validation with admin bypass
        # Admins can delete any review, regular users only their own
        if not is_admin and str(review.user_id) != current_user:
            return {'error': 'Unauthorized action'}, 403
        
        # Delete the review
        success = facade.delete_review(review_id)
        
        if success:
            return {'message': 'Review deleted successfully'}, 200
        else:
            return {'error': 'Failed to delete review'}, 400


@api.route('/places/<place_id>/reviews')
@api.param('place_id', 'The place identifier')
class PlaceReviewList(Resource):
    """
    Retrieve all reviews for a specific place (PUBLIC)
    """
    
    @api.response(200, 'List of reviews for the place')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Get all reviews for a specific place (PUBLIC - No authentication required)
        
        Args:
            place_id (str): Place's unique identifier
            
        Returns:
            list: List of reviews for the place
            dict: Error message with status 404 if place not found
            
        Example Response:
            [
                {
                    "id": "uuid-1",
                    "text": "Great place!",
                    "rating": 5,
                    "user_id": "user-uuid",
                    "place_id": "place-uuid"
                },
                ...
            ]
        """
        # Check if place exists
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Get all reviews for this place
        reviews = facade.get_reviews_by_place(place_id)
        return [review.to_dict() for review in reviews], 200