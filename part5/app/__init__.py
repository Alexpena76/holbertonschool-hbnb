"""
Application Factory for the HBnB application.
"""

import os
from flask import Flask, render_template
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Initialize extensions
bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()


def create_app(config_class="config.DevelopmentConfig"):
    """
    Create and configure the Flask application using the Application Factory pattern.
    """
    # Get the correct paths for templates and static files
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    CORS(app)
    
    # Load configuration
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    
    # Disable strict trailing slashes
    app.url_map.strict_slashes = False
    
    # =========================================================================
    # FRONTEND ROUTES - Serve HTML templates
    # =========================================================================
    
    @app.route('/')
    def index():
        """Serve the home page with places listing"""
        return render_template('index.html')
    
    @app.route('/login')
    def login():
        """Serve the login page"""
        return render_template('login.html')
    
    @app.route('/place/<place_id>')
    def place_details(place_id):
        """Serve the place details page"""
        return render_template('place.html')
    
    @app.route('/add_review/<place_id>')
    def add_review(place_id):
        """Serve the add review page"""
        return render_template('add_review.html')
    
    # =========================================================================
    # API ROUTES
    # =========================================================================
    
    # Initialize Flask-RESTX API
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/docs/'
    )
    
    # Import and register namespaces
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns
    
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    
    return app