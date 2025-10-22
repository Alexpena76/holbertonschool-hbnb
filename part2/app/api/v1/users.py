"""
User API Endpoints
Handles CRUD operations for users through RESTful API
"""

from flask_restx import Namespace, Resource, fields
from app.services import facade

# Create namespace for user operations
api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})


@api.route('/')
class UserList(Resource):
    """
    Handles operations on the user collection
    - GET: Retrieve list of all users
    - POST: Create a new user
    """
    
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """
        Retrieve a list of all users
        
        Returns:
            list: List of user dictionaries with status 200
            
        Example Response:
            [
                {
                    "id": "uuid-1",
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john.doe@example.com"
                },
                ...
            ]
        """
        # Get all users from facade
        users = facade.get_all_users()
        
        # Convert user objects to dictionaries
        return [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
            for user in users
        ], 200
    
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Register a new user
        
        Validates:
            - Email uniqueness
            - Required fields (first_name, last_name, email)
            - Field formats and lengths
        
        Returns:
            dict: Created user data with status 201
            dict: Error message with status 400 if validation fails
            
        Example Request:
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com"
            }
            
        Example Success Response:
            {
                "id": "uuid",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com"
            }
        """
        user_data = api.payload

        # Check email uniqueness
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            # Create new user through facade
            new_user = facade.create_user(user_data)
            
            # Return created user data
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201
            
        except ValueError as e:
            # Handle validation errors from User model
            return {'error': str(e)}, 400


@api.route('/<user_id>')
class UserResource(Resource):
    """
    Handles operations on individual users
    - GET: Retrieve user details by ID
    - PUT: Update user information
    """
    
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Get user details by ID
        
        Args:
            user_id (str): User's unique identifier
            
        Returns:
            dict: User data with status 200 if found
            dict: Error message with status 404 if not found
            
        Example Response:
            {
                "id": "uuid",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com"
            }
        """
        user = facade.get_user(user_id)
        
        if not user:
            return {'error': 'User not found'}, 404
        
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
    
    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'Email already registered')
    def put(self, user_id):
        """
        Update user information
        
        Args:
            user_id (str): User's unique identifier
            
        Validates:
            - User exists
            - Email uniqueness (if email is being changed)
            - Required fields and formats
            
        Returns:
            dict: Updated user data with status 200
            dict: Error message with status 404 if user not found
            dict: Error message with status 400 if validation fails
            
        Example Request:
            {
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "jane.doe@example.com"
            }
            
        Example Success Response:
            {
                "id": "uuid",
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "jane.doe@example.com"
            }
        """
        user_data = api.payload
        
        try:
            # Update user through facade
            updated_user = facade.update_user(user_id, user_data)
            
            if not updated_user:
                return {'error': 'User not found'}, 404
            
            # Return updated user data
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200
            
        except ValueError as e:
            # Handle validation errors (e.g., email already registered)
            return {'error': str(e)}, 400