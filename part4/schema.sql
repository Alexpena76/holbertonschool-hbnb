-- ============================================================
-- HBnB Database Schema
-- This script creates all tables and relationships for the HBnB application
-- ============================================================

-- Drop tables if they exist (in correct order to respect foreign keys)
DROP TABLE IF EXISTS place_amenity;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS users;

-- ============================================================
-- USERS TABLE
-- Stores user information including authentication details
-- ============================================================
CREATE TABLE users (
    -- Primary key: UUID format
    id CHAR(36) PRIMARY KEY,
    
    -- User information
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    
    -- Authentication
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE NOT NULL,
    
    -- Timestamps
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    
    -- Indexes for performance
    INDEX idx_email (email),
    INDEX idx_is_admin (is_admin)
);

-- ============================================================
-- AMENITIES TABLE
-- Stores available amenities (WiFi, Pool, etc.)
-- ============================================================
CREATE TABLE amenities (
    -- Primary key: UUID format
    id CHAR(36) PRIMARY KEY,
    
    -- Amenity information
    name VARCHAR(255) NOT NULL UNIQUE,
    
    -- Timestamps
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    
    -- Indexes for performance
    INDEX idx_name (name)
);

-- ============================================================
-- PLACES TABLE
-- Stores rental property listings
-- ============================================================
CREATE TABLE places (
    -- Primary key: UUID format
    id CHAR(36) PRIMARY KEY,
    
    -- Place information
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    
    -- Foreign key to users (owner)
    owner_id CHAR(36) NOT NULL,
    
    -- Timestamps
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    
    -- Foreign key constraints
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
    
    -- Indexes for performance
    INDEX idx_owner_id (owner_id),
    INDEX idx_price (price),
    INDEX idx_location (latitude, longitude)
);

-- ============================================================
-- REVIEWS TABLE
-- Stores user reviews for places
-- ============================================================
CREATE TABLE reviews (
    -- Primary key: UUID format
    id CHAR(36) PRIMARY KEY,
    
    -- Review content
    text TEXT NOT NULL,
    rating INT NOT NULL,
    
    -- Foreign keys
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    
    -- Timestamps
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL,
    
    -- Foreign key constraints
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    
    -- Constraints
    CHECK (rating >= 1 AND rating <= 5),
    
    -- Unique constraint: One review per user per place
    UNIQUE KEY unique_user_place (user_id, place_id),
    
    -- Indexes for performance
    INDEX idx_user_id (user_id),
    INDEX idx_place_id (place_id),
    INDEX idx_rating (rating)
);

-- ============================================================
-- PLACE_AMENITY TABLE
-- Many-to-many relationship between places and amenities
-- ============================================================
CREATE TABLE place_amenity (
    -- Foreign keys (composite primary key)
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    
    -- Composite primary key
    PRIMARY KEY (place_id, amenity_id),
    
    -- Foreign key constraints
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE,
    
    -- Indexes for performance (automatically created by foreign keys)
    INDEX idx_place_id (place_id),
    INDEX idx_amenity_id (amenity_id)
);

-- ============================================================
-- VERIFICATION QUERIES
-- Run these to verify the schema was created correctly
-- ============================================================

-- Show all tables
SHOW TABLES;

-- Show structure of each table
DESCRIBE users;
DESCRIBE amenities;
DESCRIBE places;
DESCRIBE reviews;
DESCRIBE place_amenity;