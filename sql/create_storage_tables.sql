-- =========================================================
-- Create storage_units table
-- =========================================================
-- This table stores storage units (wardrobes, closets, etc.) for each person

-- Drop table if exists (for clean recreation)
DROP TABLE IF EXISTS storage_units CASCADE;

-- Create storage_units table
CREATE TABLE storage_units (
    id SERIAL PRIMARY KEY,
    person_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    location TEXT DEFAULT '',
    description TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on person_id for faster queries
CREATE INDEX idx_storage_units_person_id ON storage_units(person_id);

-- Add foreign key constraint to users table (if users table exists)
-- Uncomment the line below if you want to enforce referential integrity:
-- ALTER TABLE storage_units ADD CONSTRAINT fk_storage_units_person FOREIGN KEY (person_id) REFERENCES users(id) ON DELETE CASCADE;

-- Display result
SELECT 'storage_units table created successfully' AS status;

-- Show table structure
\d storage_units
