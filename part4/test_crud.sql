-- ============================================================
-- HBnB CRUD Operations Testing
-- This script tests Create, Read, Update, Delete operations
-- ============================================================

-- ============================================================
-- TEST 1: CREATE OPERATIONS
-- ============================================================

-- Create a regular user
INSERT INTO users (
    id,
    first_name,
    last_name,
    email,
    password,
    is_admin
) VALUES (
    'd4e5f6a7-b8c9-40d1-e2f3-a4b5c6d7e8f9',
    'John',
    'Doe',
    'john.doe@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5aeWR5Cz.WYHi',
    FALSE
);

-- Create a place
INSERT INTO places (
    id,
    title,
    description,
    price,
    latitude,
    longitude,
    owner_id
) VALUES (
    'e5f6a7b8-c9d0-41e2-f3a4-b5c6d7e8f9a0',
    'Cozy Beach House',
    'Beautiful beach house with ocean view',
    150.00,
    34.0522,
    -118.2437,
    'd4e5f6a7-b8c9-40d1-e2f3-a4b5c6d7e8f9'
);

-- Link place to amenities
INSERT INTO place_amenity (place_id, amenity_id) VALUES
    ('e5f6a7b8-c9d0-41e2-f3a4-b5c6d7e8f9a0', 'a1b2c3d4-e5f6-47a8-b9c0-d1e2f3a4b5c6'),  -- WiFi
    ('e5f6a7b8-c9d0-41e2-f3a4-b5c6d7e8f9a0', 'b2c3d4e5-f6a7-48b9-c0d1-e2f3a4b5c6d7');  -- Pool

-- Create a review
INSERT INTO reviews (
    id,
    text,
    rating,
    user_id,
    place_id
) VALUES (
    'f6a7b8c9-d0e1-42f3-a4b5-c6d7e8f9a0b1',
    'Amazing place! Loved the ocean view.',
    5,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',  -- Admin user
    'e5f6a7b8-c9d0-41e2-f3a4-b5c6d7e8f9a0'
);

SHOW TABLES;

-- ============================================================
-- TEST 2: READ OPERATIONS
-- ============================================================

-- Read all users
SELECT 
    id,
    first_name,
    last_name,
    email,
    is_admin
FROM users;

-- Read all places with owner information
SELECT 
    p.id,
    p.title,
    p.price,
    u.first_name AS owner_first_name,
    u.last_name AS owner_last_name,
    u.email AS owner_email
FROM places p
JOIN users u ON p.owner_id = u.id;

-- Read place with its amenities
SELECT 
    p.title AS place_title,
    a.name AS amenity_name
FROM places p
JOIN place_amenity pa ON p.id = pa.place_id
JOIN amenities a ON pa.amenity_id = a.id
WHERE p.id = 'e5f6a7b8-c9d0-41e2-f3a4-b5c6d7e8f9a0';

-- Read reviews with user and place information
SELECT 
    r.id,
    r.text,
    r.rating,
    u.first_name AS reviewer_first_name,
    u.last_name AS reviewer_last_name,
    p.title AS place_title
FROM reviews r
JOIN users u ON r.user_id = u.id
JOIN places p ON r.place_id = p.id;

-- ============================================================
-- TEST 3: UPDATE OPERATIONS
-- ============================================================

-- Update user information
UPDATE users
SET 
    first_name = 'Jane',
    last_name = 'Smith',
    updated_at = CURRENT_TIMESTAMP
WHERE email = 'john.doe@example.com';

-- Verify update
SELECT 
    id,
    first_name,
    last_name,
    email,
    updated_at
FROM users
WHERE email = 'john.doe@example.com';

-- Update place price
UPDATE places
SET 
    price = 175.00,
    updated_at = CURRENT_TIMESTAMP
WHERE id = 'e5f6a7b8-c9d0-41e2-f3a4-b5c6d7e8f9a0';

-- Verify update
SELECT 
    id,
    title,
    price,
    updated_at
FROM places
WHERE id = 'e5f6a7b8-c9d0-41e2-f3a4-b5c6d7e8f9a0';

-- Update review rating
UPDATE reviews
SET 
    rating = 4,
    text = 'Great place! Minor issues but overall excellent.',
    updated_at = CURRENT_TIMESTAMP
WHERE id = 'f6a7b8c9-d0e1-42f3-a4b5-c6d7e8f9a0b1';

-- Verify update
SELECT 
    id,
    text,
    rating,
    updated_at
FROM reviews
WHERE id = 'f6a7b8c9-d0e1-42f3-a4b5-c6d7e8f9a0b1';

-- ============================================================
-- TEST 4: DELETE OPERATIONS
-- ============================================================

-- Delete a review
DELETE FROM reviews
WHERE id = 'f6a7b8c9-d0e1-42f3-a4b5-c6d7e8f9a0b1';

-- Verify deletion
SELECT COUNT(*) AS review_count
FROM reviews
WHERE id = 'f6a7b8c9-d0e1-42f3-a4b5-c6d7e8f9a0b1';

-- Delete place (should cascade to place_amenity)
DELETE FROM places
WHERE id = 'e5f6a7b8-c9d0-41e2-f3a4-b5c6d7e8f9a0';

-- Verify deletion and cascade
SELECT COUNT(*) AS place_count
FROM places
WHERE id = 'e5f6a7b8-c9d0-41e2-f3a4-b5c6d7e8f9a0';

SELECT COUNT(*) AS place_amenity_count
FROM place_amenity
WHERE place_id = 'e5f6a7b8-c9d0-41e2-f3a4-b5c6d7e8f9a0';

-- Delete user
DELETE FROM users
WHERE email = 'john.doe@example.com';

-- Verify deletion
SELECT COUNT(*) AS user_count
FROM users
WHERE email = 'john.doe@example.com';

-- ============================================================
-- TEST 5: CONSTRAINT TESTING
-- ============================================================

-- Test unique email constraint (should fail)
-- Uncomment to test:
-- INSERT INTO users (id, first_name, last_name, email, password)
-- VALUES ('test-id', 'Test', 'User', 'admin@hbnb.io', 'password123');

-- Test rating constraint (should fail)
-- Uncomment to test:
-- INSERT INTO reviews (id, text, rating, user_id, place_id)
-- VALUES ('test-id', 'Test review', 6, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'e5f6a7b8-c9d0-41e2-f3a4-b5c6d7e8f9a0');

-- Test unique review per user per place (should fail)
-- Uncomment to test:
-- First create a place and review, then try to create duplicate:
-- INSERT INTO reviews (id, text, rating, user_id, place_id)
-- VALUES ('test-id-2', 'Another review', 5, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'e5f6a7b8-c9d0-41e2-f3a4-b5c6d7e8f9a0');

-- ============================================================
-- FINAL VERIFICATION
-- ============================================================

-- Show final state of all tables
SELECT 'Users:' AS info;
SELECT id, first_name, last_name, email, is_admin FROM users;

SELECT 'Amenities:' AS info;
SELECT id, name FROM amenities;

SELECT 'Places:' AS info;
SELECT id, title, price FROM places;

SELECT 'Reviews:' AS info;
SELECT id, rating, user_id, place_id FROM reviews;

SELECT 'Place-Amenity Relationships:' AS info;
SELECT place_id, amenity_id FROM place_amenity;