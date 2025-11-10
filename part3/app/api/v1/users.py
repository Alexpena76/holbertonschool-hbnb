"""
User API Endpoints
Handles CRUD operations for users through RESTful API
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt  # ADMIN ADDITION: Added get_jwt
from app.services import facade

# Create namespace for user operations
api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user (min 6 chars)')
})


@api.route('/')
class UserList(Resource):
    """
    Handles operations on the user collection
    - GET: Retrieve list of all users
    - POST: Create a new user (ADMIN ONLY)  # ADMIN ADDITION: Now requires admin
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
        
        # Use to_dict() to exclude passwords
        return [user.to_dict() for user in users], 200
    
    @jwt_required()  # ADMIN ADDITION: Now requires authentication
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid input')
    @api.response(403, 'Admin privileges required')  # ADMIN ADDITION: New error response
    def post(self):
        """
        Register a new user (ADMIN ONLY)
        
        ADMIN ADDITION: This endpoint is now restricted to administrators only.
        Regular users cannot create new user accounts through the API.
        
        Validates:
            - Email uniqueness
            - Required fields (first_name, last_name, email, password)
            - Field formats and lengths
            - Admin privileges
        
        Returns:
            dict: Created user data with status 201
            dict: Error message with status 400 if validation fails
            dict: Error message with status 403 if not admin
            
        Example Request:
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "password": "securepass123"
            }
            
        Example Success Response:
            {
                "id": "uuid",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com"
            }
        """
        # ADMIN ADDITION: Check if user is admin
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        if not is_admin:
            return {'error': 'Admin privileges required'}, 403
        
        user_data = api.payload

        # Validate password
        if not user_data.get('password'):
            return {'error': 'Password is required'}, 400
        
        if len(user_data.get('password', '')) < 6:
            return {'error': 'Password must be at least 6 characters long'}, 400

        # Check email uniqueness
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            # Create new user through facade (password will be hashed)
            new_user = facade.create_user(user_data)
            
            # Use to_dict() to exclude password
            return new_user.to_dict(), 201
            
        except ValueError as e:
            # Handle validation errors from User model
            return {'error': str(e)}, 400


@api.route('/<user_id>')
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    """
    Handles operations on individual users
    - GET: Retrieve user details by ID
    - PUT: Update user information (AUTHENTICATED - Own profile or ADMIN)
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
        
        # Use to_dict() to exclude password
        return user.to_dict(), 200
    
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data or attempt to modify email/password')
    @api.response(403, 'Unauthorized action')
    @api.response(401, 'Unauthorized - Invalid or missing token')
    def put(self, user_id):
        """
        Update user information (Own profile or ADMIN)
        
        ADMIN ADDITION: Administrators can now:
        - Modify ANY user's profile (not just their own)
        - Change email addresses (with uniqueness validation)
        - Change passwords
        
        Regular users can still only modify their own profile,
        but cannot change email or password.
        
        Args:
            user_id (str): User's unique identifier
            
        Returns:
            dict: Updated user data with status 200
            dict: Error message with status 404 if user not found
            dict: Error message with status 400 if trying to modify email/password (regular users)
            dict: Error message with status 400 if email already in use
            dict: Error message with status 403 if trying to modify another user's data (regular users)
            
        Example Request (Regular User):
            Headers:
                Authorization: Bearer <jwt_token>
            Body:
                {
                    "first_name": "Jane",
                    "last_name": "Doe"
                }
                
        Example Request (Admin):
            Headers:
                Authorization: Bearer <admin_jwt_token>
            Body:
                {
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "email": "newemail@example.com",
                    "password": "newpassword123"
                }
                
        Example Success Response:
            {
                "id": "uuid",
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "jane.doe@example.com"
            }
            
        Example Error Responses:
            {"error": "Unauthorized action"} - 403 (regular user trying to modify another user)
            {"error": "You cannot modify email or password"} - 400 (regular user trying to change email/password)
            {"error": "Email already in use"} - 400 (admin trying to set duplicate email)
        """
        current_user = get_jwt_identity()
        
        # ADMIN ADDITION: Get admin status from JWT claims
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # ADMIN ADDITION: Check authorization - admin can modify anyone, users only themselves
        if not is_admin and current_user != user_id:
            return {'error': 'Unauthorized action'}, 403
        
        user_data = api.payload
        
        # ADMIN ADDITION: Only non-admins are restricted from changing email/password
        if not is_admin:
            # Regular users cannot modify email
            if 'email' in user_data:
                return {'error': 'You cannot modify email or password'}, 400
            
            # Regular users cannot modify password
            if 'password' in user_data:
                return {'error': 'You cannot modify email or password'}, 400
        else:
            # ADMIN ADDITION: Admins can change email, but must check uniqueness
            if 'email' in user_data:
                new_email = user_data['email']
                existing_user = facade.get_user_by_email(new_email)
                if existing_user and existing_user.id != user_id:
                    return {'error': 'Email already in use'}, 400
        
        try:
            # Update user through facade
            updated_user = facade.update_user(user_id, user_data)
            
            if not updated_user:
                return {'error': 'User not found'}, 404
            
            # Use to_dict() to exclude password
            return updated_user.to_dict(), 200
            
        except ValueError as e:
            # Handle validation errors
            return {'error': str(e)}, 400