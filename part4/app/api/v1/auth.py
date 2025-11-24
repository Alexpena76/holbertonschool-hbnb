"""
Authentication API endpoints
Handles user login and JWT token generation
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.services import facade

# Create namespace for authentication operations
api = Namespace('auth', description='Authentication operations')

# Model for login input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/login')
class Login(Resource):
    """
    Handles user login and JWT token generation
    """
    
    @api.expect(login_model, validate=True)
    @api.response(200, 'Login successful, JWT token returned')
    @api.response(401, 'Invalid credentials')
    @api.response(400, 'Missing required fields')
    def post(self):
        """
        Authenticate user and return a JWT token
        
        This endpoint:
        1. Receives email and password from the client
        2. Validates the credentials against stored user data
        3. Generates a JWT token with user identity and claims
        4. Returns the token to the client for subsequent authenticated requests
        
        Example Request:
            {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        
        Example Success Response:
            {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
            }
        
        The JWT token contains:
            - identity: user ID
            - is_admin: boolean flag indicating admin status
            - exp: expiration timestamp
        """
        credentials = api.payload
        
        # Step 1: Retrieve the user based on the provided email
        user = facade.get_user_by_email(credentials['email'])
        
        # Step 2: Check if the user exists and the password is correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401
        
        # Step 3: Create a JWT token with the user's id and is_admin flag
        access_token = create_access_token(
            identity=str(user.id),  # User ID as the token identity
            additional_claims={
                "is_admin": user.is_admin  # Include admin status in token
            }
        )
        
        # Step 4: Return the JWT token to the client
        return {
            'access_token': access_token
        }, 200


@api.route('/protected')
class ProtectedResource(Resource):
    """
    Example protected endpoint that requires JWT authentication
    This demonstrates how to protect routes and access user information from tokens
    """
    
    @jwt_required()
    @api.response(200, 'Access granted')
    @api.response(401, 'Missing or invalid token')
    def get(self):
        """
        A protected endpoint that requires a valid JWT token
        
        This endpoint demonstrates:
        - How to protect routes with @jwt_required()
        - How to extract user identity from the token
        - How to access additional claims (like is_admin)
        
        The token must be sent in the Authorization header:
            Authorization: Bearer <your_jwt_token>
        
        Example Response:
            {
                "message": "Hello, user 3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "is_admin": false
            }
        """
        # Get the user identity (user ID) from the token
        current_user_id = get_jwt_identity()
        
        # Get additional claims from the token
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        return {
            'message': f'Hello, user {current_user_id}',
            'is_admin': is_admin
        }, 200