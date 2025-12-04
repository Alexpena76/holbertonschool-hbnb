# HBnB Application - Part 4

## Overview

HBnB is a full-stack Flask-based REST API application that implements a vacation rental platform similar to Airbnb. The application follows a layered architecture with clear separation between Presentation, Business Logic, Service, and Persistence layers. It uses the **Repository Pattern**, **Facade Pattern**, and **SQLAlchemy ORM** for database persistence.

### Key Features
- **RESTful API** with Flask-RESTX and Swagger documentation
- **JWT Authentication** for secure user sessions
- **Bcrypt Password Hashing** for security
- **SQLAlchemy ORM** with SQLite database
- **Repository Pattern** for data access abstraction
- **Facade Pattern** for business logic coordination

---

## Project Structure

```
part4/
├── run.py                              # Application entry point
├── config.py                           # Configuration (Dev/Test/Prod)
├── requirements.txt                    # Python dependencies
├── schema.sql                          # Database schema
├── populate_test_data.sql              # Sample data for testing
├── app/
│   ├── __init__.py                     # Flask app factory
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py                 # Authentication endpoints
│   │       ├── users.py                # User CRUD endpoints
│   │       ├── places.py               # Place CRUD endpoints
│   │       ├── reviews.py              # Review CRUD endpoints
│   │       └── amenities.py            # Amenity CRUD endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py               # Base model with id, timestamps
│   │   ├── user.py                     # User model
│   │   ├── place.py                    # Place model
│   │   ├── review.py                   # Review model
│   │   └── amenity.py                  # Amenity model
│   ├── services/
│   │   ├── __init__.py                 # Facade singleton
│   │   ├── facade.py                   # Business logic coordinator
│   │   └── repositories/
│   │       ├── __init__.py
│   │       ├── user_repository.py      # User-specific queries
│   │       ├── place_repository.py     # Place-specific queries
│   │       ├── review_repository.py    # Review-specific queries
│   │       └── amenity_repository.py   # Amenity-specific queries
│   └── persistence/
│       ├── __init__.py
│       └── repository.py               # Base repository classes
├── templates/                          # Jinja2 HTML templates
│   ├── index.html                      # Homepage with place listings
│   ├── login.html                      # Login page
│   ├── place.html                      # Place details page
│   └── add_review.html                 # Add review page
├── static/
│   ├── css/
│   │   └── styles.css                  # Application styles
│   └── js/
│       └── script.js                   # Frontend JavaScript (login)
└── tests/
    ├── __init__.py
    ├── test_user_endpoints.py
    ├── test_place_endpoints.py
    ├── test_review_endpoints.py
    ├── test_amenity_endpoints.py
    ├── test_authenticated_endpoints.py
    ├── test_admin_endpoints.py
    ├── test_jwt.py
    └── test_passwords.py
```

---

## Architecture

### Layer Organization

```
┌─────────────────────────────────────────────────────────┐
│              Presentation Layer (API)                    │
│                    Flask-RESTX                           │
│         auth.py, users.py, places.py, reviews.py         │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                 Service Layer (Facade)                   │
│              Business Logic Coordination                 │
│                     facade.py                            │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│              Business Logic Layer (Models)               │
│              Validation & Domain Rules                   │
│         user.py, place.py, review.py, amenity.py         │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│             Persistence Layer (Repositories)             │
│               SQLAlchemy ORM + SQLite                    │
│    repository.py + user_repository.py, etc.              │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

```
HTTP Request → API Endpoint → Facade → Repository → SQLite Database
                    ↓
              JWT Validation (if protected route)
                    ↓
              Model Validation
                    ↓
              Database Operation
                    ↓
HTTP Response ← JSON Response ← to_dict() ← Model Object
```

---

## Database Schema

### Entity Relationships

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│    User      │       │    Place     │       │   Amenity    │
├──────────────┤       ├──────────────┤       ├──────────────┤
│ id (PK)      │──┐    │ id (PK)      │    ┌──│ id (PK)      │
│ first_name   │  │    │ title        │    │  │ name         │
│ last_name    │  │    │ description  │    │  └──────────────┘
│ email        │  │    │ price        │    │
│ password     │  └───►│ owner_id(FK) │    │  ┌──────────────┐
│ is_admin     │       │ latitude     │◄───┼──│place_amenity │
└──────────────┘       │ longitude    │    │  ├──────────────┤
       │               └──────────────┘    │  │place_id (FK) │
       │                      │            └──│amenity_id(FK)│
       │                      │               └──────────────┘
       │               ┌──────▼───────┐
       │               │    Review    │
       │               ├──────────────┤
       └──────────────►│ id (PK)      │
                       │ text         │
                       │ rating       │
                       │ user_id (FK) │
                       │ place_id(FK) │
                       └──────────────┘
```

### Relationships
- **User → Place**: One-to-Many (user owns many places)
- **User → Review**: One-to-Many (user writes many reviews)
- **Place → Review**: One-to-Many (place has many reviews)
- **Place ↔ Amenity**: Many-to-Many (via `place_amenity` junction table)

---

## Authentication

### JWT Token Flow

1. **Login**: `POST /api/v1/auth/login` with email and password
2. **Receive Token**: Server returns JWT access token
3. **Use Token**: Include in header: `Authorization: Bearer <token>`
4. **Access Protected Routes**: Token is validated on each request

### Token Structure
```
Header:    {"alg": "HS256", "typ": "JWT"}
Payload:   {"identity": "user-id", "is_admin": false, "exp": timestamp}
Signature: HMACSHA256(header + payload, JWT_SECRET_KEY)
```

### Password Security
- Passwords are hashed using **Bcrypt** before storage
- Minimum 6 characters required
- Passwords are **never** returned in API responses

---

## API Endpoints

### Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/login` | User login, returns JWT | No |
| GET | `/api/v1/auth/protected` | Test protected route | Yes |

### Users
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/users/` | List all users | No |
| GET | `/api/v1/users/<id>` | Get user by ID | No |
| POST | `/api/v1/users/` | Create new user | No |
| PUT | `/api/v1/users/<id>` | Update user | Yes |
| DELETE | `/api/v1/users/<id>` | Delete user | Yes (Admin) |

### Places
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/places/` | List all places | No |
| GET | `/api/v1/places/<id>` | Get place by ID | No |
| POST | `/api/v1/places/` | Create new place | Yes |
| PUT | `/api/v1/places/<id>` | Update place | Yes (Owner/Admin) |
| DELETE | `/api/v1/places/<id>` | Delete place | Yes (Owner/Admin) |

### Reviews
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/reviews/` | List all reviews | No |
| GET | `/api/v1/reviews/<id>` | Get review by ID | No |
| POST | `/api/v1/reviews/` | Create new review | Yes |
| PUT | `/api/v1/reviews/<id>` | Update review | Yes (Author/Admin) |
| DELETE | `/api/v1/reviews/<id>` | Delete review | Yes (Author/Admin) |

### Amenities
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/amenities/` | List all amenities | No |
| GET | `/api/v1/amenities/<id>` | Get amenity by ID | No |
| POST | `/api/v1/amenities/` | Create new amenity | Yes (Admin) |
| PUT | `/api/v1/amenities/<id>` | Update amenity | Yes (Admin) |
| DELETE | `/api/v1/amenities/<id>` | Delete amenity | Yes (Admin) |

---

## Configuration

### Environment Classes

| Setting | Development | Testing | Production |
|---------|-------------|---------|------------|
| DEBUG | True | True | False |
| JWT Expiration | 24 hours | 5 minutes | 1 hour |
| Database | development.db | testing.db | PostgreSQL |
| Secure Cookies | No | No | Yes |

### Environment Variables
```bash
# Set these in production
export SECRET_KEY="your-super-secret-key"
export JWT_SECRET_KEY="your-jwt-secret-key"
export DATABASE_URL="postgresql://user:pass@host/db"
```

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/Alexpena76/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part4

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize the database
sqlite3 instance/development.db < schema.sql

# 5. (Optional) Populate with test data
sqlite3 instance/development.db < populate_test_data.sql

# 6. Run the application
python run.py
```

### Access Points
- **API Documentation (Swagger)**: http://127.0.0.1:5000/api/v1/
- **Homepage**: http://127.0.0.1:5000/ (if frontend routes configured)

---

## Testing

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run Specific Test Files
```bash
python -m pytest tests/test_user_endpoints.py -v
python -m pytest tests/test_jwt.py -v
python -m pytest tests/test_passwords.py -v
```

### Test Coverage
```bash
python -m pytest tests/ --cov=app --cov-report=html
```

---

## Test User Credentials

From `populate_test_data.sql`:

| Email | Password | Admin |
|-------|----------|-------|
| admin@hbnb.io | admin1234 | Yes |
| john.doe@example.com | password123 | No |
| jane.smith@example.com | password123 | No |
| bob.wilson@example.com | password123 | No |
| alice.johnson@example.com | password123 | No |

---

## Design Patterns

### 1. Repository Pattern
Abstracts data persistence, allowing easy swap between storage implementations.

```python
# Base class in repository.py
class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model  # Receives model class (User, Place, etc.)
    
    def get_all(self):
        return self.model.query.all()

# Specific repository extends it
class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)  # Pass User model to parent
    
    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()
```

### 2. Facade Pattern
Provides unified interface for business logic coordination.

```python
class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        # ... coordinates all repositories
```

### 3. Factory Pattern
Creates configured Flask application instances.

```python
def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # ... configure extensions and routes
    return app
```

---

## Security Features

### SQL Injection Prevention
SQLAlchemy ORM uses parameterized queries automatically:
```python
# Safe - SQLAlchemy escapes input
user = User.query.filter_by(email=email).first()
```

### Password Security
- Bcrypt hashing with salt
- Minimum length validation
- Passwords excluded from API responses via `to_dict()`

### JWT Security
- Tokens signed with secret key
- Expiration timestamps
- Admin claims for authorization

### Authorization Checks
- Ownership verification for updates/deletes
- Admin-only routes for amenity management
- Prevention of ownership transfer attacks

---

## Current Limitations

- Frontend templates use static/hardcoded data (not fetching from API dynamically)
- No image upload functionality
- No search/filtering on places
- No pagination for large result sets
- No email verification
- No password reset functionality

---

## Future Improvements

- [ ] Dynamic frontend with JavaScript API calls
- [ ] Image uploads for places
- [ ] Search and filtering
- [ ] Pagination
- [ ] Email verification
- [ ] Password reset
- [ ] Rate limiting
- [ ] Caching layer
- [ ] Docker containerization

---

## Author

**Alejandro Peña**

---

## License

This project is part of the Holberton School HBnB Evolution curriculum.