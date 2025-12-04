# HBnB Evolution - Part 4

A full-stack vacation rental platform API built with Flask, similar to Airbnb. Features JWT authentication, SQLAlchemy ORM, role-based access control, and a complete RESTful API.

---

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Database Schema](#database-schema)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Authorization & Permissions](#authorization--permissions)
- [Test Data](#test-data)
- [Testing](#testing)
- [Frontend](#frontend)
- [Design Patterns](#design-patterns)
- [Security Features](#security-features)
- [Author](#author)

---

## Features

- **User Management**: Registration, authentication, profile updates
- **Place Listings**: Create, read, update, delete rental properties
- **Reviews System**: Users can review places (with validation rules)
- **Amenities**: Admin-managed amenities linked to places
- **JWT Authentication**: Secure token-based authentication
- **Role-Based Access Control**: Admin vs regular user permissions
- **Password Security**: Bcrypt hashing with salt
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| **Framework** | Flask 3.0.0 |
| **API** | Flask-RESTX 1.3.0 (with Swagger docs) |
| **Database** | SQLite with Flask-SQLAlchemy 3.1.1 |
| **Authentication** | Flask-JWT-Extended 4.6.0 |
| **Password Hashing** | Flask-Bcrypt 1.0.1 |
| **CORS** | Flask-CORS 4.0.0 |
| **Validation** | jsonschema 4.17.3 |

---

## Project Structure

```
part4/
├── run.py                              # Application entry point
├── config.py                           # Environment configurations
├── create_admin.py                     # Script to create admin user
├── generate_bcrypt_hash.py             # Utility for password hashing
├── requirements.txt                    # Python dependencies
├── schema.sql                          # Database schema definition
├── populate_test_data.sql              # Sample data (5 users, 5 places, 8 amenities, 9 reviews)
├── app/
│   ├── __init__.py                     # Flask app factory + extensions
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py                 # Login, protected routes
│   │       ├── users.py                # User CRUD (admin-restricted creation)
│   │       ├── places.py               # Place CRUD (owner/admin permissions)
│   │       ├── reviews.py              # Review CRUD (author/admin permissions)
│   │       └── amenities.py            # Amenity CRUD (admin only)
│   ├── models/
│   │   ├── __init__.py                 # Association table (place_amenity)
│   │   ├── base_model.py               # Abstract base with id, timestamps
│   │   ├── user.py                     # User model + password hashing
│   │   ├── place.py                    # Place model + relationships
│   │   ├── review.py                   # Review model + validation
│   │   └── amenity.py                  # Amenity model
│   ├── services/
│   │   ├── __init__.py                 # Facade singleton instance
│   │   ├── facade.py                   # Business logic coordinator
│   │   └── repositories/
│   │       ├── __init__.py
│   │       ├── user_repository.py      # get_user_by_email()
│   │       ├── place_repository.py     # get_by_owner()
│   │       ├── review_repository.py    # get_by_place(), get_by_user()
│   │       └── amenity_repository.py   # get_by_name()
│   └── persistence/
│       ├── __init__.py
│       └── repository.py               # Repository, InMemoryRepository, SQLAlchemyRepository
├── templates/
│   ├── index.html                      # Homepage with place cards
│   ├── login.html                      # Login form
│   ├── place.html                      # Place details + reviews
│   └── add_review.html                 # Review submission form
├── static/
│   ├── css/
│   │   └── styles.css                  # Complete styling (responsive)
│   └── js/
│       └── script.js                   # Login functionality + JWT cookie handling
└── tests/
    ├── __init__.py
    ├── test_user_endpoints.py
    ├── test_place_endpoints.py
    ├── test_review_endpoints.py
    ├── test_amenity_endpoints.py
    ├── test_authenticated_endpoints.py
    ├── test_admin_endpoints.py
    ├── test_jwt.py                     # JWT flow testing
    └── test_passwords.py
```

---

## Architecture

### Layered Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER                         │
│                      (API Endpoints)                         │
│         auth.py | users.py | places.py | reviews.py          │
│                      Flask-RESTX                             │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    SERVICE LAYER                             │
│                      (Facade)                                │
│                     facade.py                                │
│            Business logic coordination                       │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                 BUSINESS LOGIC LAYER                         │
│                      (Models)                                │
│         user.py | place.py | review.py | amenity.py          │
│              Validation & domain rules                       │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                  PERSISTENCE LAYER                           │
│                   (Repositories)                             │
│   SQLAlchemyRepository → UserRepo, PlaceRepo, ReviewRepo     │
│                  SQLite Database                             │
└─────────────────────────────────────────────────────────────┘
```

### Request Flow

```
HTTP Request
     │
     ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  API Route  │ ──► │   Facade    │ ──► │ Repository  │ ──► │  Database   │
│ (places.py) │     │ (facade.py) │     │ (SQLAlchemy)│     │  (SQLite)   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
     │                                                              │
     │◄─────────────────── JSON Response ◄──────────────────────────┘
     │
     ▼
HTTP Response
```

---

## Database Schema

### Entity Relationship Diagram

```
┌─────────────────┐
│      users      │
├─────────────────┤
│ id (PK)         │──────────────────────────────┐
│ first_name      │                              │
│ last_name       │                              │
│ email (unique)  │                              │
│ password        │                              │
│ is_admin        │                              │
│ created_at      │                              │
│ updated_at      │                              │
└─────────────────┘                              │
        │                                        │
        │ 1:N                                    │ 1:N
        ▼                                        │
┌─────────────────┐                              │
│     places      │                              │
├─────────────────┤                              │
│ id (PK)         │──────────────┐               │
│ title           │              │               │
│ description     │              │               │
│ price           │              │               │
│ latitude        │              │               │
│ longitude       │              │               │
│ owner_id (FK)───┼──► users.id  │               │
│ created_at      │              │               │
│ updated_at      │              │               │
└─────────────────┘              │               │
        │                        │               │
        │ N:N                    │ 1:N           │
        ▼                        │               │
┌─────────────────┐              │               │
│  place_amenity  │              │               │
├─────────────────┤              │               │
│ place_id (FK)───┼──► places.id │               │
│ amenity_id (FK)─┼──► amenities.id              │
└─────────────────┘              │               │
        │                        │               │
        │                        ▼               │
        │              ┌─────────────────┐       │
        │              │    reviews      │       │
        │              ├─────────────────┤       │
        │              │ id (PK)         │       │
        │              │ text            │       │
        │              │ rating (1-5)    │       │
        │              │ user_id (FK)────┼───────┘
        │              │ place_id (FK)───┼──► places.id
        │              │ created_at      │
        │              │ updated_at      │
        │              └─────────────────┘
        │
        ▼
┌─────────────────┐
│   amenities     │
├─────────────────┤
│ id (PK)         │
│ name (unique)   │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

### Relationships Summary

| Relationship | Type | Description |
|--------------|------|-------------|
| User → Places | One-to-Many | User owns many places |
| User → Reviews | One-to-Many | User writes many reviews |
| Place → Reviews | One-to-Many | Place has many reviews |
| Place ↔ Amenity | Many-to-Many | Via `place_amenity` junction table |

---

## Installation

### Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

### Setup Steps

```bash
# 1. Clone the repository
git clone https://github.com/Alexpena76/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part4

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize the database with schema
sqlite3 instance/development.db < schema.sql

# 5. Populate with test data (optional but recommended)
sqlite3 instance/development.db < populate_test_data.sql

# 6. Run the application
python run.py
```

### Access Points

| URL | Description |
|-----|-------------|
| http://127.0.0.1:5000/api/v1/ | Swagger API Documentation |
| http://127.0.0.1:5000/api/v1/places/ | Places API |
| http://127.0.0.1:5000/api/v1/users/ | Users API |

---

## Configuration

### Environment Classes (config.py)

| Setting | Development | Testing | Production |
|---------|-------------|---------|------------|
| `DEBUG` | True | True | False |
| `JWT_ACCESS_TOKEN_EXPIRES` | 24 hours | 5 minutes | 1 hour |
| `SQLALCHEMY_DATABASE_URI` | sqlite:///development.db | sqlite:///testing.db | PostgreSQL (env var) |
| `SESSION_COOKIE_SECURE` | False | False | True |

### Environment Variables

```bash
# Production settings (set these in your environment)
export SECRET_KEY="your-very-secure-secret-key"
export JWT_SECRET_KEY="your-jwt-secret-key"
export DATABASE_URL="postgresql://user:password@host:port/database"
```

---

## API Endpoints

### Authentication (`/api/v1/auth`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/login` | Authenticate user, return JWT | No |
| GET | `/protected` | Test protected route | Yes |

### Users (`/api/v1/users`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | List all users | No |
| POST | `/` | Create user | **Admin only** |
| GET | `/<id>` | Get user by ID | No |
| PUT | `/<id>` | Update user | Yes (self or Admin) |

### Places (`/api/v1/places`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | List all places | No |
| POST | `/` | Create place | Yes |
| GET | `/<id>` | Get place by ID | No |
| PUT | `/<id>` | Update place | Yes (owner or Admin) |

### Reviews (`/api/v1/reviews`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | List all reviews | No |
| POST | `/` | Create review | Yes |
| GET | `/<id>` | Get review by ID | No |
| PUT | `/<id>` | Update review | Yes (author or Admin) |
| DELETE | `/<id>` | Delete review | Yes (author or Admin) |
| GET | `/places/<place_id>/reviews` | Get reviews for place | No |

### Amenities (`/api/v1/amenities`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | List all amenities | No |
| POST | `/` | Create amenity | **Admin only** |
| GET | `/<id>` | Get amenity by ID | No |
| PUT | `/<id>` | Update amenity | **Admin only** |

---

## Authentication

### JWT Token Flow

```
1. POST /api/v1/auth/login
   Body: {"email": "user@example.com", "password": "password123"}
   
2. Response: {"access_token": "eyJhbGciOiJIUzI1NiIs..."}

3. Use token in subsequent requests:
   Header: Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### Token Structure

```
┌─────────────────────────────────────────────────────────┐
│                      JWT TOKEN                           │
├─────────────────────────────────────────────────────────┤
│ HEADER    │ {"alg": "HS256", "typ": "JWT"}              │
├───────────┼─────────────────────────────────────────────┤
│ PAYLOAD   │ {                                           │
│           │   "identity": "user-uuid",                  │
│           │   "is_admin": false,                        │
│           │   "exp": 1234567890                         │
│           │ }                                           │
├───────────┼─────────────────────────────────────────────┤
│ SIGNATURE │ HMACSHA256(header + payload, JWT_SECRET)    │
└───────────┴─────────────────────────────────────────────┘
```

### Password Security

Passwords are hashed using Bcrypt before storage:

```python
# Registration (user.py)
def hash_password(self, password):
    self.password = bcrypt.generate_password_hash(password).decode('utf-8')

# Login verification
def verify_password(self, password):
    return bcrypt.check_password_hash(self.password, password)
```

---

## Authorization & Permissions

### Role-Based Access Control

| Action | Regular User | Admin |
|--------|--------------|-------|
| Create user | ❌ | ✅ |
| Update own profile | ✅ | ✅ |
| Update other's profile | ❌ | ✅ |
| Change email/password | ❌ | ✅ |
| Create place | ✅ | ✅ |
| Update own place | ✅ | ✅ |
| Update any place | ❌ | ✅ |
| Create review | ✅ | ✅ |
| Review own place | ❌ | ❌ |
| Update own review | ✅ | ✅ |
| Update any review | ❌ | ✅ |
| Delete own review | ✅ | ✅ |
| Delete any review | ❌ | ✅ |
| Manage amenities | ❌ | ✅ |

### Review Validation Rules

1. **Cannot review own place**: Users cannot review places they own
2. **One review per place**: Users can only review each place once

---

## Test Data

After running `populate_test_data.sql`:

### Users

| Name | Email | Password | Admin |
|------|-------|----------|-------|
| Admin User | admin@hbnb.io | admin1234 | ✅ |
| John Doe | john.doe@example.com | password123 | ❌ |
| Jane Smith | jane.smith@example.com | password123 | ❌ |
| Bob Wilson | bob.wilson@example.com | password123 | ❌ |
| Alice Johnson | alice.johnson@example.com | password123 | ❌ |

### Places

| Title | Price | Owner |
|-------|-------|-------|
| Beautiful Beach House | $150 | Admin |
| Cozy Mountain Cabin | $120 | John Doe |
| Modern City Apartment | $200 | Jane Smith |
| Lakefront Paradise | $180 | Bob Wilson |
| Desert Oasis Villa | $250 | Alice Johnson |

### Amenities

WiFi, Swimming Pool, Air Conditioning, Parking, Kitchen, Gym, Hot Tub, TV

### Reviews

9 sample reviews distributed across places with ratings 3-5 stars.

---

## Testing

### Run All Tests

```bash
python -m pytest tests/ -v
```

### Run Specific Tests

```bash
# JWT authentication tests
python -m pytest tests/test_jwt.py -v

# User endpoint tests
python -m pytest tests/test_user_endpoints.py -v

# Admin functionality tests
python -m pytest tests/test_admin_endpoints.py -v
```

### Manual JWT Test

```bash
python tests/test_jwt.py
```

---

## Frontend

### Current Implementation

The frontend consists of static HTML templates with CSS styling and JavaScript for login functionality.

| File | Purpose |
|------|---------|
| `index.html` | Homepage with place cards (static) |
| `login.html` | Login form with JavaScript validation |
| `place.html` | Place details page (static) |
| `add_review.html` | Review submission form |
| `styles.css` | Complete responsive styling |
| `script.js` | Login flow, JWT cookie management |

### JavaScript Features (script.js)

- Form validation (email format, required fields)
- API login request handling
- JWT token storage in cookies (7-day expiration)
- Authentication status checking
- Error/success message display
- `authenticatedFetch()` helper for protected requests

### Note on Frontend

The HTML templates currently display **static/hardcoded data**. The API is fully functional and returns dynamic data from the database. To make the frontend dynamic, JavaScript would need to fetch data from the API endpoints.

---

## Design Patterns

### 1. Repository Pattern

Abstracts data access, enabling easy swap between storage implementations.

```python
# Base class
class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model
    
    def get_all(self):
        return self.model.query.all()

# Entity-specific repository
class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)  # Pass User model to parent
    
    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()
```

### 2. Facade Pattern

Provides a unified interface for business logic coordination.

```python
class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()
    
    def create_place(self, place_data):
        # Validate owner exists
        owner = self.user_repo.get(place_data['owner_id'])
        if not owner:
            raise ValueError('Owner not found')
        # Create and save place
        place = Place(**place_data)
        self.place_repo.add(place)
        return place
```

### 3. Factory Pattern

Creates configured Flask application instances.

```python
def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    
    # Register API namespaces
    # ...
    
    return app
```

---

## Security Features

### SQL Injection Prevention

SQLAlchemy ORM uses parameterized queries:

```python
# Safe - SQLAlchemy escapes all input
user = User.query.filter_by(email=user_input).first()

# Generates: SELECT * FROM users WHERE email = ? (parameterized)
```

### Password Security

- Bcrypt hashing with automatic salt
- Minimum 6 character requirement
- Passwords never returned in API responses (`to_dict()` excludes password)

### JWT Security

- Tokens signed with secret key (HMAC-SHA256)
- Configurable expiration times
- Admin claims embedded in token
- Automatic rejection of expired/invalid tokens

### Authorization Checks

- Ownership verification before updates/deletes
- Admin bypass for administrative actions
- Prevention of ownership transfer attacks (owner_id stripped from updates)

---

## Author

**Alejandro Peña**

---

## License

This project is part of the Holberton School HBnB Evolution curriculum.