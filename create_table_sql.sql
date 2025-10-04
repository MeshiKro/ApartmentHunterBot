-- SQL to create the properties table in Supabase
-- Run this in your Supabase Dashboard > SQL Editor

CREATE TABLE IF NOT EXISTS properties (
    id SERIAL PRIMARY KEY,
    description TEXT,
    address TEXT,
    price DECIMAL(10,2),
    rooms INTEGER,
    size DECIMAL(8,2),
    phone TEXT,
    city TEXT,
    url TEXT,
    sent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert sample data to test
INSERT INTO properties (description, address, price, rooms, size, phone, city, url, sent) 
VALUES 
('Beautiful 3-bedroom apartment in Tel Aviv', 'Rothschild Boulevard 1', 15000.00, 3, 85.5, '+972-50-123-4567', 'Tel Aviv', 'https://example.com/property/1', false),
('Modern 2-bedroom apartment in Jerusalem', 'King George Street 10', 12000.00, 2, 65.0, '+972-50-987-6543', 'Jerusalem', 'https://example.com/property/2', false),
('Spacious 4-bedroom house in Haifa', 'Herzl Street 25', 18000.00, 4, 120.0, '+972-50-555-1234', 'Haifa', 'https://example.com/property/3', false);

-- Verify the table was created
SELECT * FROM properties;
