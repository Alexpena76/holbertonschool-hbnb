"""
Flask application entry point
Runs the HBnB API server
"""
import sys
import os

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

from app import create_app

# Create the Flask application instance
app = create_app()

if __name__ == '__main__':
    # Run the development server
    print("=" * 60)
    print("Starting HBnB API Server")
    print("=" * 60)
    print(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"Project Directory: {project_dir}")
    print("=" * 60)
    print("\nAPI will be available at:")
    print("  - http://127.0.0.1:5000")
    print("  - http://localhost:5000")
    print("\nAPI Documentation (Swagger):")
    print("  - http://127.0.0.1:5000/api/v1/")
    print("\nPress CTRL+C to quit\n")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
