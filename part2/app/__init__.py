"""
Flask Application Factory - UPDATED
Creates and configures the Flask application instance
"""

from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns

def create_app():
    """
    Application factory function
    
    Returns:
        Flask: Configured Flask application instance with registered namespaces
    """
    app = Flask(__name__)
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    
    # Future namespaces will be added here:
    # api.add_namespace(places_ns, path='/api/v1/places')
    # api.add_namespace(reviews_ns, path='/api/v1/reviews')
    # api.add_namespace(amenities_ns, path='/api/v1/amenities')

    return app


# ==================== TESTING GUIDE ====================
"""
TESTING YOUR API ENDPOINTS

1. Start the Flask Application:
   cd ~/holbertonschool-hbnb/part2
   python run.py

2. The API will be available at: http://localhost:5000
   Documentation at: http://localhost:5000/api/v1/

3. Test with cURL:

   A. Create a User (POST):
   curl -X POST http://localhost:5000/api/v1/users/ \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "John",
       "last_name": "Doe",
       "email": "john.doe@example.com"
     }'
   
   Expected: 201 Created with user data including ID
   
   B. Get All Users (GET):
   curl -X GET http://localhost:5000/api/v1/users/
   
   Expected: 200 OK with array of all users
   
   C. Get User by ID (GET):
   curl -X GET http://localhost:5000/api/v1/users/<user_id>
   
   Replace <user_id> with actual ID from creation response
   Expected: 200 OK with user data
   
   D. Update User (PUT):
   curl -X PUT http://localhost:5000/api/v1/users/<user_id> \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "Jane",
       "last_name": "Smith",
       "email": "jane.smith@example.com"
     }'
   
   Expected: 200 OK with updated user data
   
   E. Test Error Cases:
   
   # Duplicate email
   curl -X POST http://localhost:5000/api/v1/users/ \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "Test",
       "last_name": "User",
       "email": "john.doe@example.com"
     }'
   Expected: 400 Bad Request - Email already registered
   
   # Invalid email format
   curl -X POST http://localhost:5000/api/v1/users/ \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "Test",
       "last_name": "User",
       "email": "notanemail"
     }'
   Expected: 400 Bad Request - Invalid email format
   
   # User not found
   curl -X GET http://localhost:5000/api/v1/users/invalid-id
   Expected: 404 Not Found
   
   # Missing required fields
   curl -X POST http://localhost:5000/api/v1/users/ \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "Test"
     }'
   Expected: 400 Bad Request - Missing required fields

4. Test with Postman:
   - Import the endpoints into Postman
   - Use the same request bodies as shown in cURL examples
   - Check response status codes and bodies

5. Use Swagger UI:
   - Navigate to http://localhost:5000/api/v1/
   - Interactive API documentation
   - Test endpoints directly from browser
"""