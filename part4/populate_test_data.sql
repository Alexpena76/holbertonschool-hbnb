-- ============================================================
-- HBnB Test Data Population
-- Creates sample users, amenities, places, and reviews
-- ============================================================

-- ============================================================
-- USERS (Already have admin, add more test users)
-- ============================================================

INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at) VALUES
-- Test User 1 (password: password123)
('550e8400-e29b-41d4-a716-446655440001', 'John', 'Doe', 'john.doe@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5aeWR5Cz.WYHi', FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Test User 2 (password: password123)
('550e8400-e29b-41d4-a716-446655440002', 'Jane', 'Smith', 'jane.smith@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5aeWR5Cz.WYHi', FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Test User 3 (password: password123)
('550e8400-e29b-41d4-a716-446655440003', 'Bob', 'Wilson', 'bob.wilson@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5aeWR5Cz.WYHi', FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Test User 4 (password: password123)
('550e8400-e29b-41d4-a716-446655440004', 'Alice', 'Johnson', 'alice.johnson@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5aeWR5Cz.WYHi', FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- ============================================================
-- AMENITIES
-- ============================================================

INSERT INTO amenities (id, name, created_at, updated_at) VALUES
('a1b2c3d4-e5f6-47a8-b9c0-d1e2f3a4b5c6', 'WiFi', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('b2c3d4e5-f6a7-48b9-c0d1-e2f3a4b5c6d7', 'Swimming Pool', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('c3d4e5f6-a7b8-49c0-d1e2-f3a4b5c6d7e8', 'Air Conditioning', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('d4e5f6a7-b8c9-40d1-e2f3-a4b5c6d7e8f9', 'Parking', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('e5f6a7b8-c9d0-41e2-f3a4-b5c6d7e8f9a0', 'Kitchen', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('f6a7b8c9-d0e1-42f3-a4b5-c6d7e8f9a0b1', 'Gym', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('a7b8c9d0-e1f2-43a4-b5c6-d7e8f9a0b1c2', 'Hot Tub', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('b8c9d0e1-f2a3-44b5-c6d7-e8f9a0b1c2d3', 'TV', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- ============================================================
-- PLACES
-- ============================================================

INSERT INTO places (id, title, description, price, latitude, longitude, owner_id, created_at, updated_at) VALUES
-- Beach House (owned by Admin)
('e5f6a7b8-c9d0-41e2-f3a4-b5c6d7e8f9a0', 
 'Beautiful Beach House', 
 'A stunning beach house with ocean views and modern amenities. Perfect for families and groups.', 
 150.00, 
 34.0522, 
 -118.2437, 
 '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 
 CURRENT_TIMESTAMP, 
 CURRENT_TIMESTAMP),

-- Mountain Cabin (owned by John Doe)
('f6a7b8c9-d0e1-42f3-a4b5-c6d7e8f9a0b1', 
 'Cozy Mountain Cabin', 
 'Secluded cabin in the mountains with breathtaking views. Great for hiking and relaxation.', 
 120.00, 
 39.7392, 
 -104.9903, 
 '550e8400-e29b-41d4-a716-446655440001', 
 CURRENT_TIMESTAMP, 
 CURRENT_TIMESTAMP),

-- City Apartment (owned by Jane Smith)
('a7b8c9d0-e1f2-43a4-b5c6-d7e8f9a0b1c2', 
 'Modern City Apartment', 
 'Downtown apartment with great access to restaurants and nightlife. Walking distance to metro.', 
 200.00, 
 40.7128, 
 -74.0060, 
 '550e8400-e29b-41d4-a716-446655440002', 
 CURRENT_TIMESTAMP, 
 CURRENT_TIMESTAMP),

-- Lake House (owned by Bob Wilson)
('b8c9d0e1-f2a3-44b5-c6d7-e8f9a0b1c2d3', 
 'Lakefront Paradise', 
 'Beautiful house right on the lake with private dock. Perfect for water activities.', 
 180.00, 
 44.9778, 
 -93.2650, 
 '550e8400-e29b-41d4-a716-446655440003', 
 CURRENT_TIMESTAMP, 
 CURRENT_TIMESTAMP),

-- Desert Villa (owned by Alice Johnson)
('c9d0e1f2-a3b4-45c6-d7e8-f9a0b1c2d3e4', 
 'Desert Oasis Villa', 
 'Luxury villa in the desert with pool and stunning sunset views.', 
 250.00, 
 33.4484, 
 -112.0740, 
 '550e8400-e29b-41d4-a716-446655440004', 
 CURRENT_TIMESTAMP, 
 CURRENT_TIMESTAMP);

-- ============================================================
-- PLACE_AMENITY (Link places to amenities)
-- ============================================================

INSERT INTO place_amenity (place_id, amenity_id) VALUES
-- Beach House amenities
('e5f6a7b8-c9d0-41e2-f3a4-b5c6d7e8f9a0', 'a1b2c3d4-e5f6-47a8-b9c0-d1e2f3a4b5c6'),  -- WiFi
('e5f6a7b8-c9d0-41e2-f3a4-b5c6d7e8f9a0', 'b2c3d4e5-f6a7-48b9-c0d1-e2f3a4b5c6d7'),  -- Pool
('e5f6a7b8-c9d0-41e2-f3a4-b5c6d7e8f9a0', 'c3d4e5f6-a7b8-49c0-d1e2-f3a4b5c6d7e8'),  -- AC
('e5f6a7b8-c9d0-41e2-f3a4-b5c6d7e8f9a0', 'd4e5f6a7-b8c9-40d1-e2f3-a4b5c6d7e8f9'),  -- Parking
('e5f6a7b8-c9d0-41e2-f3a4-b5c6d7e8f9a0', 'e5f6a7b8-c9d0-41e2-f3a4-b5c6d7e8f9a0'),  -- Kitchen

-- Mountain Cabin amenities
('f6a7b8c9-d0e1-42f3-a4b5-c6d7e8f9a0b1', 'a1b2c3d4-e5f6-47a8-b9c0-d1e2f3a4b5c6'),  -- WiFi
('f6a7b8c9-d0e1-42f3-a4b5-c6d7e8f9a0b1', 'e5f6a7b8-c9d0-41e2-f3a4-b5c6d7e8f9a0'),  -- Kitchen
('f6a7b8c9-d0e1-42f3-a4b5-c6d7e8f9a0b1', 'd4e5f6a7-b8c9-40d1-e2f3-a4b5c6d7e8f9'),  -- Parking
('f6a7b8c9-d0e1-42f3-a4b5-c6d7e8f9a0b1', 'a7b8c9d0-e1f2-43a4-b5c6-d7e8f9a0b1c2'),  -- Hot Tub

-- City Apartment amenities
('a7b8c9d0-e1f2-43a4-b5c6-d7e8f9a0b1c2', 'a1b2c3d4-e5f6-47a8-b9c0-d1e2f3a4b5c6'),  -- WiFi
('a7b8c9d0-e1f2-43a4-b5c6-d7e8f9a0b1c2', 'c3d4e5f6-a7b8-49c0-d1e2-f3a4b5c6d7e8'),  -- AC
('a7b8c9d0-e1f2-43a4-b5c6-d7e8f9a0b1c2', 'f6a7b8c9-d0e1-42f3-a4b5-c6d7e8f9a0b1'),  -- Gym
('a7b8c9d0-e1f2-43a4-b5c6-d7e8f9a0b1c2', 'b8c9d0e1-f2a3-44b5-c6d7-e8f9a0b1c2d3'),  -- TV

-- Lake House amenities
('b8c9d0e1-f2a3-44b5-c6d7-e8f9a0b1c2d3', 'a1b2c3d4-e5f6-47a8-b9c0-d1e2f3a4b5c6'),  -- WiFi
('b8c9d0e1-f2a3-44b5-c6d7-e8f9a0b1c2d3', 'e5f6a7b8-c9d0-41e2-f3a4-b5c6d7e8f9a0'),  -- Kitchen
('b8c9d0e1-f2a3-44b5-c6d7-e8f9a0b1c2d3', 'd4e5f6a7-b8c9-40d1-e2f3-a4b5c6d7e8f9'),  -- Parking
('b8c9d0e1-f2a3-44b5-c6d7-e8f9a0b1c2d3', 'b8c9d0e1-f2a3-44b5-c6d7-e8f9a0b1c2d3'),  -- TV

-- Desert Villa amenities
('c9d0e1f2-a3b4-45c6-d7e8-f9a0b1c2d3e4', 'a1b2c3d4-e5f6-47a8-b9c0-d1e2f3a4b5c6'),  -- WiFi
('c9d0e1f2-a3b4-45c6-d7e8-f9a0b1c2d3e4', 'b2c3d4e5-f6a7-48b9-c0d1-e2f3a4b5c6d7'),  -- Pool
('c9d0e1f2-a3b4-45c6-d7e8-f9a0b1c2d3e4', 'c3d4e5f6-a7b8-49c0-d1e2-f3a4b5c6d7e8'),  -- AC
('c9d0e1f2-a3b4-45c6-d7e8-f9a0b1c2d3e4', 'd4e5f6a7-b8c9-40d1-e2f3-a4b5c6d7e8f9'),  -- Parking
('c9d0e1f2-a3b4-45c6-d7e8-f9a0b1c2d3e4', 'e5f6a7b8-c9d0-41e2-f3a4-b5c6d7e8f9a0'),  -- Kitchen
('c9d0e1f2-a3b4-45c6-d7e8-f9a0b1c2d3e4', 'a7b8c9d0-e1f2-43a4-b5c6-d7e8f9a0b1c2');  -- Hot Tub

-- ============================================================
-- REVIEWS
-- ============================================================

INSERT INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at) VALUES
-- Reviews for Beach House
('r1000000-0000-0000-0000-000000000001', 
 'Amazing beach house! The views were spectacular and the amenities were top-notch.', 
 5, 
 '550e8400-e29b-41d4-a716-446655440001', 
 'e5f6a7b8-c9d0-41e2-f3a4-b5c6d7e8f9a0', 
 CURRENT_TIMESTAMP, 
 CURRENT_TIMESTAMP),

('r1000000-0000-0000-0000-000000000002', 
 'Great location, very clean. Only downside was some noise from neighbors.', 
 4, 
 '550e8400-e29b-41d4-a716-446655440002', 
 'e5f6a7b8-c9d0-41e2-f3a4-b5c6d7e8f9a0', 
 CURRENT_TIMESTAMP, 
 CURRENT_TIMESTAMP),

-- Reviews for Mountain Cabin
('r1000000-0000-0000-0000-000000000003', 
 'Perfect getaway! So peaceful and the hot tub was a nice touch.', 
 5, 
 '550e8400-e29b-41d4-a716-446655440002', 
 'f6a7b8c9-d0e1-42f3-a4b5-c6d7e8f9a0b1', 
 CURRENT_TIMESTAMP, 
 CURRENT_TIMESTAMP),

('r1000000-0000-0000-0000-000000000004', 
 'Nice cabin but a bit remote. WiFi was spotty.', 
 3, 
 '550e8400-e29b-41d4-a716-446655440003', 
 'f6a7b8c9-d0e1-42f3-a4b5-c6d7e8f9a0b1', 
 CURRENT_TIMESTAMP, 
 CURRENT_TIMESTAMP),

-- Reviews for City Apartment
('r1000000-0000-0000-0000-000000000005', 
 'Excellent location! Walking distance to everything.', 
 5, 
 '550e8400-e29b-41d4-a716-446655440001', 
 'a7b8c9d0-e1f2-43a4-b5c6-d7e8f9a0b1c2', 
 CURRENT_TIMESTAMP, 
 CURRENT_TIMESTAMP),

('r1000000-0000-0000-0000-000000000006', 
 'Great apartment but can be noisy at night due to downtown location.', 
 4, 
 '550e8400-e29b-41d4-a716-446655440004', 
 'a7b8c9d0-e1f2-43a4-b5c6-d7e8f9a0b1c2', 
 CURRENT_TIMESTAMP, 
 CURRENT_TIMESTAMP),

-- Reviews for Lake House
('r1000000-0000-0000-0000-000000000007', 
 'Beautiful lake views and great for water activities. Highly recommend!', 
 5, 
 '550e8400-e29b-41d4-a716-446655440003', 
 'b8c9d0e1-f2a3-44b5-c6d7-e8f9a0b1c2d3', 
 CURRENT_TIMESTAMP, 
 CURRENT_TIMESTAMP),

-- Reviews for Desert Villa
('r1000000-0000-0000-0000-000000000008', 
 'Absolutely stunning! The sunsets from the pool were unforgettable.', 
 5, 
 '550e8400-e29b-41d4-a716-446655440001', 
 'c9d0e1f2-a3b4-45c6-d7e8-f9a0b1c2d3e4', 
 CURRENT_TIMESTAMP, 
 CURRENT_TIMESTAMP),

('r1000000-0000-0000-0000-000000000009', 
 'Luxury at its finest but quite expensive.', 
 4, 
 '550e8400-e29b-41d4-a716-446655440002', 
 'c9d0e1f2-a3b4-45c6-d7e8-f9a0b1c2d3e4', 
 CURRENT_TIMESTAMP, 
 CURRENT_TIMESTAMP);

-- ============================================================
-- VERIFICATION QUERIES
-- ============================================================

-- Count all records
SELECT 'users' AS table_name, COUNT(*) AS count FROM users
UNION ALL
SELECT 'amenities', COUNT(*) FROM amenities
UNION ALL
SELECT 'places', COUNT(*) FROM places
UNION ALL
SELECT 'reviews', COUNT(*) FROM reviews
UNION ALL
SELECT 'place_amenity', COUNT(*) FROM place_amenity;
