-- ============================================================
-- HBnB Initial Data Population
-- This script inserts the administrator user and initial amenities
-- ============================================================

-- ============================================================
-- INSERT ADMINISTRATOR USER
-- Fixed UUID: 36c9050e-ddd3-4c3b-9731-9f487208bbc1
-- Password: admin1234 (hashed with bcrypt)
-- ============================================================

INSERT INTO users (
    id,
    first_name,
    last_name,
    email,
    password,
    is_admin,
    created_at,
    updated_at
) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    -- Bcrypt hash of 'admin1234'
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5aeWR5Cz.WYHi',
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- ============================================================
-- INSERT INITIAL AMENITIES
-- UUIDs generated for each amenity
-- ============================================================

INSERT INTO amenities (id, name, created_at, updated_at) VALUES
    -- WiFi
    ('a1b2c3d4-e5f6-47a8-b9c0-d1e2f3a4b5c6', 'WiFi', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    
    -- Swimming Pool
    ('b2c3d4e5-f6a7-48b9-c0d1-e2f3a4b5c6d7', 'Swimming Pool', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    
    -- Air Conditioning
    ('c3d4e5f6-a7b8-49c0-d1e2-f3a4b5c6d7e8', 'Air Conditioning', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- ============================================================
-- VERIFICATION QUERIES
-- Run these to verify the data was inserted correctly
-- ============================================================

-- Verify admin user
SELECT 
    id,
    first_name,
    last_name,
    email,
    is_admin,
    created_at
FROM users
WHERE email = 'admin@hbnb.io';

-- Verify amenities
SELECT 
    id,
    name,
    created_at
FROM amenities
ORDER BY name;

-- Count records
SELECT 
    'users' AS table_name, 
    COUNT(*) AS record_count 
FROM users
UNION ALL
SELECT 
    'amenities' AS table_name, 
    COUNT(*) AS record_count 
FROM amenities;