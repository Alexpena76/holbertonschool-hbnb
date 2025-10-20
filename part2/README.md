# HBnB Application - Code Documentation

## Overview
This is a Flask-based REST API application that implements a vacation rental platform similar to AirBnB, the application follows a layered architecture with clear separation between Presentation, Business Logic, Service, and Persistence layers. It uses the Repository and Facade patterns to ensure maintainability, scalability, and loose coupling between components

## Code Structure
The implementation consists of a modular design organized across multiple layers:
```
hbnb/
nano README.md├── run.py (Entry Point)
├── config.py (Configuration)
├── requirements.txt (Dependencies)
└── app/
    ├── __init__.py (Flask App Factory)
    ├── api/
    │   └── v1/
    │       ├── users.py (User Endpoints)
    │       ├── places.py (Place Endpoints)
    │       ├── reviews.py (Review Endpoints)
    │       └── amenities.py (Amenity Endpoints)
    ├── models/
    │   ├── user.py (User Business Logic)
    │   ├── place.py (Place Business Logic)
    │   ├── review.py (Review Business Logic)
    │   └── amenity.py (Amenity Business Logic)
    ├── services/
    │   └── facade.py (Facade Pattern)
    └── persistence/
        └── repository.py (Repository Pattern)
```

## Architecture Overview

### Layer Organization
```
┌─────────────────────────────────────┐
│     Presentation Layer (API)        │
│         Flask-RESTX                 │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Service Layer (Facade)         │
│    Coordinates Business Logic       │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Business Logic Layer (Models)     │
│   Validation & Domain Rules         │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│   Persistence Layer (Repository)    │
│     Data Storage Abstraction        │
└─────────────────────────────────────┘
```

## Component Documentation

### 1. `run.py` - Application Entry Point
**Purpose:** Initializes and runs the Flask application

**Key Operations:**
- Imports application factory from `app` module
- Creates Flask application instance
- Starts development server with debug mode

**Usage:**
```bash
python run.py
```

**Server Configuration:**
- Host: `127.0.0.1`
- Port: `5000`
- Debug Mode: Enabled (development)
- API Documentation: `http://127.0.0.1:5000/api/v1/`

---

### 2. `config.py` - Configuration Management
**Purpose:** Manages environment-specific application settings

**Configuration Classes:**

#### `Config` (Base Configuration)
- `SECRET_KEY`: Application secret key for sessions
- `DEBUG`: Debug mode flag (default: False)

#### `DevelopmentConfig` (Development Settings)
- Inherits from `Config`
- `DEBUG`: True (enables detailed error pages)

**Configuration Dictionary:**
```python
config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
```

**Environment Variables:**
- `SECRET_KEY`: Override default secret key

---

### 3. `app/__init__.py` - Flask Application Factory
**Purpose:** Creates and configures Flask application instance

**Function:** `create_app()`

**Return:** Configured Flask application object

**Configuration Process:**
1. Initialize Flask application
2. Create Flask-RESTX API instance
3. Configure API metadata (version, title, description)
4. Set API documentation endpoint (`/api/v1/`)
5. Register API namespaces (placeholders for future endpoints)

**API Metadata:**
- Version: `1.0`
- Title: `HBnB API`
- Description: `HBnB Application API`
- Documentation: `/api/v1/`

---

### 4. `app/persistence/repository.py` - Repository Pattern Implementation

#### `Repository` (Abstract Base Class)
**Purpose:** Defines interface for data persistence operations

**Abstract Methods:**

##### `add(obj)`
**Purpose:** Store a new object
**Parameters:** `obj` - Object to store
**Returns:** None

##### `get(obj_id)`
**Purpose:** Retrieve object by ID
**Parameters:** `obj_id` - Unique identifier
**Returns:** Object if found, None otherwise

##### `get_all()`
**Purpose:** Retrieve all stored objects
**Returns:** List of all objects

##### `update(obj_id, data)`
**Purpose:** Update existing object
**Parameters:**
- `obj_id`: Object identifier
- `data`: Dictionary of fields to update

##### `delete(obj_id)`
**Purpose:** Remove object from storage
**Parameters:** `obj_id` - Object identifier

##### `get_by_attribute(attr_name, attr_value)`
**Purpose:** Find object by specific attribute
**Parameters:**
- `attr_name`: Attribute name to search
- `attr_value`: Value to match
**Returns:** First matching object or None

---

#### `InMemoryRepository` (Concrete Implementation)
**Purpose:** Provides in-memory storage using Python dictionary

**Internal Structure:**
```python
self._storage = {}  # Dictionary: {obj_id: obj}
```

**Implementation Details:**

##### `__init__()`
- Initializes empty storage dictionary

##### `add(obj)`
**Algorithm:**
1. Extract object ID
2. Store object in dictionary with ID as key

##### `get(obj_id)`
**Algorithm:**
1. Use dict.get() to safely retrieve object
2. Return object or None if not found

##### `get_all()`
**Algorithm:**
1. Extract all values from storage dictionary
2. Convert to list and return

##### `update(obj_id, data)`
**Algorithm:**
1. Retrieve object using get()
2. If object exists, call its update() method
3. Pass data dictionary to object's update method

##### `delete(obj_id)`
**Algorithm:**
1. Check if ID exists in storage
2. Delete entry from dictionary if found

##### `get_by_attribute(attr_name, attr_value)`
**Algorithm:**
1. Iterate through all stored objects
2. Use getattr() to access specified attribute
3. Compare attribute value with search value
4. Return first match using next() with generator

---

### 5. `app/services/facade.py` - Facade Pattern Implementation

#### `HBnBFacade` Class
**Purpose:** Provides unified interface to subsystems and coordinates operations

**Repository Management:**
```python
self.user_repo = InMemoryRepository()
self.place_repo = InMemoryRepository()
self.review_repo = InMemoryRepository()
self.amenity_repo = InMemoryRepository()
```

**Design Benefits:**
- Single point of access for all business operations
- Encapsulates complexity of inter-layer communication
- Simplifies API layer implementation
- Centralizes business logic coordination

**Placeholder Methods:**

##### `create_user(user_data)`
**Purpose:** Handle user creation logic
**Parameters:** `user_data` - Dictionary containing user information
**Status:** Placeholder (implementation in future tasks)

##### `get_place(place_id)`
**Purpose:** Retrieve place by identifier
**Parameters:** `place_id` - Place unique identifier
**Status:** Placeholder (implementation in future tasks)

**Future Methods:**
- `create_place()`, `update_place()`, `delete_place()`
- `create_review()`, `update_review()`, `delete_review()`
- `create_amenity()`, `update_amenity()`, `delete_amenity()`
- Business logic validation methods
- Cross-entity relationship management

---

### 6. `app/services/__init__.py` - Facade Singleton
**Purpose:** Creates single instance of Facade for application-wide use

**Singleton Pattern:**
```python
facade = HBnBFacade()
```

**Usage in API Endpoints:**
```python
from app.services import facade

# In route handler
user = facade.create_user(user_data)
```

**Benefits:**
- Ensures single source of truth
- Prevents multiple repository instances
- Simplifies dependency injection
- Maintains consistent state across requests

---

## Data Flow Architecture

### Request Processing Flow
```
HTTP Request
    │
    ▼
┌─────────────────────┐
│  API Endpoint       │ ← Flask-RESTX Route
│  (users.py)         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Facade             │ ← facade.create_user()
│  (facade.py)        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Business Logic     │ ← User Model Validation
│  (user.py)          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Repository         │ ← user_repo.add()
│  (repository.py)    │
└──────────┬──────────┘
           │
           ▼
    In-Memory Storage
    (Dictionary)
```

---

## Project Setup Instructions

### Prerequisites
- Python 3.7+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation Steps

#### 1. Create Project Directory Structure
```bash
mkdir -p hbnb/app/{api/v1,models,services,persistence}
cd hbnb
```

#### 2. Create All Required Files
Create empty `__init__.py` files in:
- `app/__init__.py`
- `app/api/__init__.py`
- `app/api/v1/__init__.py`
- `app/models/__init__.py`
- `app/services/__init__.py`
- `app/persistence/__init__.py`

Create placeholder files:
- `app/api/v1/users.py`
- `app/api/v1/places.py`
- `app/api/v1/reviews.py`
- `app/api/v1/amenities.py`
- `app/models/user.py`
- `app/models/place.py`
- `app/models/review.py`
- `app/models/amenity.py`

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Required Packages:**
- `flask`: Web framework
- `flask-restx`: REST API extension with Swagger documentation

#### 4. Run the Application
```bash
python run.py
```

#### 5. Access API Documentation
Open browser and navigate to:
```
http://127.0.0.1:5000/api/v1/
```

---

## Testing the Initial Setup

### Verify Flask Application
```bash
python run.py
```

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Test API Documentation
```bash
curl http://127.0.0.1:5000/api/v1/
```

**Expected:** Swagger UI interface loads successfully

### Verify Import Structure
```python
# Test in Python shell
from app import create_app
from app.services import facade
from app.persistence.repository import InMemoryRepository

print("All imports successful!")
```

---

## Design Patterns Used

### 1. Repository Pattern
**Purpose:** Abstracts data persistence logic

**Benefits:**
- Decouples business logic from data storage
- Easy to swap storage implementations
- Consistent interface for data operations
- Simplifies testing with mock repositories

**Implementation:**
- Abstract base class defines contract
- Concrete class implements in-memory storage
- Future: Database implementation using SQLAlchemy

### 2. Facade Pattern
**Purpose:** Simplifies complex subsystem interactions

**Benefits:**
- Reduces coupling between layers
- Provides simple interface to complex operations
- Centralizes business logic coordination
- Makes API endpoints cleaner and more maintainable

### 3. Factory Pattern
**Purpose:** Creates application instances

**Benefits:**
- Configurable application creation
- Supports multiple configurations
- Enables testing with different settings
- Clean separation of concerns

---

## Future Development Roadmap

### Part 2: Business Logic & API Implementation
- Implement User, Place, Review, Amenity models
- Add validation logic and business rules
- Create RESTful API endpoints
- Implement CRUD operations
- Add error handling and status codes

### Part 3: Database Integration
- Replace InMemoryRepository with SQLAlchemy
- Design database schema
- Implement migrations
- Add database-backed persistence
- Configure connection pooling

### Part 4: Advanced Features
- User authentication and authorization
- Search and filtering functionality
- Pagination for large result sets
- File uploads for place images
- Rating and review systems

---

## Code Quality Standards

### Compilation/Execution
```bash
# Run application
python run.py

# Run with specific configuration
FLASK_ENV=development python run.py
```

### Testing Checklist
- ✓ Flask application starts without errors
- ✓ API documentation accessible at `/api/v1/`
- ✓ All imports resolve correctly
- ✓ Repository methods work with test data
- ✓ Facade singleton creates successfully
- ✓ No memory leaks in long-running process

---

## File Structure Reference

### Complete Directory Tree
```
hbnb/
├── run.py                          # Application entry point
├── config.py                       # Configuration management
├── requirements.txt                # Python dependencies
├── README.md                       # This documentation
└── app/                            # Main application package
    ├── __init__.py                 # Flask app factory
    ├── api/                        # Presentation layer
    │   ├── __init__.py
    │   └── v1/                     # API version 1
    │       ├── __init__.py
    │       ├── users.py            # User endpoints
    │       ├── places.py           # Place endpoints
    │       ├── reviews.py          # Review endpoints
    │       └── amenities.py        # Amenity endpoints
    ├── models/                     # Business logic layer
    │   ├── __init__.py
    │   ├── user.py                 # User model
    │   ├── place.py                # Place model
    │   ├── review.py               # Review model
    │   └── amenity.py              # Amenity model
    ├── services/                   # Service layer
    │   ├── __init__.py             # Facade singleton
    │   └── facade.py               # Facade implementation
    └── persistence/                # Persistence layer
        ├── __init__.py
        └── repository.py           # Repository implementation
```

---

## Limitations (Current Version)
- No authentication or authorization
- No database persistence (in-memory only)
- No input validation in API layer
- No error handling implementation
- No logging configuration
- No unit tests included
- No API endpoints implemented yet
- No business logic models implemented

---

## Contributing Guidelines
1. Follow PEP 8 style guidelines
2. Add docstrings to all functions and classes
3. Write unit tests for new features
4. Update documentation for API changes
5. Use type hints where applicable
6. Keep layers properly separated

---

## Author
**Alejandro Peña**

---

## License
This project is part of the HBnB application development curriculum.

---
