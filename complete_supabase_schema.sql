-- =====================================================
-- COMPLETE SUPABASE DATABASE SCHEMA FOR APARTMENT HUNTER BOT
-- =====================================================
-- Run this entire script in your Supabase Dashboard > SQL Editor
-- This creates all the tables needed for your application

-- =====================================================
-- 1. PROPERTIES TABLE (Main apartment listings)
-- =====================================================
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

-- =====================================================
-- 2. POSTS TABLE (ETL processed posts from MongoDB)
-- =====================================================
CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    mongo_id TEXT UNIQUE,
    content TEXT NOT NULL,
    rooms DECIMAL(5,2),
    size DECIMAL(8,2),
    price DECIMAL(10,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- 3. SCHEDULES TABLE (Scraping schedule configuration)
-- =====================================================
CREATE TABLE IF NOT EXISTS schedules (
    id SERIAL PRIMARY KEY,
    start_time TIME,
    end_time TIME,
    start_date DATE,
    end_date DATE,
    start_option TEXT, -- 'immediately', 'on-date', 'on-time'
    end_option TEXT,   -- 'never', 'on-date', 'after-count'
    max_posts INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- 4. SCRAPING_LOGS TABLE (Track scraping activities)
-- =====================================================
CREATE TABLE IF NOT EXISTS scraping_logs (
    id SERIAL PRIMARY KEY,
    run_id TEXT UNIQUE,
    start_time TIMESTAMP WITH TIME ZONE,
    end_time TIMESTAMP WITH TIME ZONE,
    posts_found INTEGER DEFAULT 0,
    posts_processed INTEGER DEFAULT 0,
    posts_saved INTEGER DEFAULT 0,
    status TEXT, -- 'running', 'completed', 'failed'
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- 5. EMAIL_NOTIFICATIONS TABLE (Track sent notifications)
-- =====================================================
CREATE TABLE IF NOT EXISTS email_notifications (
    id SERIAL PRIMARY KEY,
    recipient_email TEXT NOT NULL,
    subject TEXT,
    posts_count INTEGER,
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status TEXT DEFAULT 'sent' -- 'sent', 'failed'
);

-- =====================================================
-- 6. USER_SETTINGS TABLE (Application settings)
-- =====================================================
CREATE TABLE IF NOT EXISTS user_settings (
    id SERIAL PRIMARY KEY,
    setting_key TEXT UNIQUE NOT NULL,
    setting_value TEXT,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- 7. FACEBOOK_GROUPS TABLE (Track monitored groups)
-- =====================================================
CREATE TABLE IF NOT EXISTS facebook_groups (
    id SERIAL PRIMARY KEY,
    group_name TEXT NOT NULL,
    group_url TEXT UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_scraped TIMESTAMP WITH TIME ZONE,
    posts_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- 8. INDEXES FOR BETTER PERFORMANCE
-- =====================================================

-- Properties table indexes
CREATE INDEX IF NOT EXISTS idx_properties_created_at ON properties(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_properties_city ON properties(city);
CREATE INDEX IF NOT EXISTS idx_properties_price ON properties(price);
CREATE INDEX IF NOT EXISTS idx_properties_sent ON properties(sent);

-- Posts table indexes
CREATE INDEX IF NOT EXISTS idx_posts_mongo_id ON posts(mongo_id);
CREATE INDEX IF NOT EXISTS idx_posts_created_at ON posts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_posts_price ON posts(price);

-- Schedules table indexes
CREATE INDEX IF NOT EXISTS idx_schedules_active ON schedules(is_active);
CREATE INDEX IF NOT EXISTS idx_schedules_created_at ON schedules(created_at DESC);

-- Scraping logs indexes
CREATE INDEX IF NOT EXISTS idx_scraping_logs_run_id ON scraping_logs(run_id);
CREATE INDEX IF NOT EXISTS idx_scraping_logs_status ON scraping_logs(status);
CREATE INDEX IF NOT EXISTS idx_scraping_logs_created_at ON scraping_logs(created_at DESC);

-- Email notifications indexes
CREATE INDEX IF NOT EXISTS idx_email_notifications_recipient ON email_notifications(recipient_email);
CREATE INDEX IF NOT EXISTS idx_email_notifications_sent_at ON email_notifications(sent_at DESC);

-- Facebook groups indexes
CREATE INDEX IF NOT EXISTS idx_facebook_groups_url ON facebook_groups(group_url);
CREATE INDEX IF NOT EXISTS idx_facebook_groups_active ON facebook_groups(is_active);

-- =====================================================
-- 9. SAMPLE DATA INSERTION
-- =====================================================

-- Insert sample properties
INSERT INTO properties (description, address, price, rooms, size, phone, city, url, sent) 
VALUES 
('Beautiful 3-bedroom apartment in Tel Aviv', 'Rothschild Boulevard 1', 15000.00, 3, 85.5, '+972-50-123-4567', 'Tel Aviv', 'https://example.com/property/1', false),
('Modern 2-bedroom apartment in Jerusalem', 'King George Street 10', 12000.00, 2, 65.0, '+972-50-987-6543', 'Jerusalem', 'https://example.com/property/2', false),
('Spacious 4-bedroom house in Haifa', 'Herzl Street 25', 18000.00, 4, 120.0, '+972-50-555-1234', 'Haifa', 'https://example.com/property/3', false),
('Cozy 1-bedroom studio in Netanya', 'Herzl Street 5', 8000.00, 1, 45.0, '+972-50-777-8888', 'Netanya', 'https://example.com/property/4', false),
('Luxury 5-bedroom villa in Herzliya', 'Ramat Yam 15', 25000.00, 5, 200.0, '+972-50-999-0000', 'Herzliya', 'https://example.com/property/5', false);

-- Insert sample posts
INSERT INTO posts (mongo_id, content, rooms, size, price) 
VALUES 
('mongo_id_1', 'Amazing 3-room apartment in the heart of Tel Aviv with sea view', 3, 85.5, 15000.00),
('mongo_id_2', 'Beautiful 2-room apartment near the beach in Netanya', 2, 65.0, 12000.00),
('mongo_id_3', 'Spacious 4-room house with garden in Haifa', 4, 120.0, 18000.00);

-- Insert default schedule
INSERT INTO schedules (start_time, end_time, start_option, end_option, is_active) 
VALUES 
('09:00:00', '18:00:00', 'immediately', 'never', true);

-- Insert default user settings
INSERT INTO user_settings (setting_key, setting_value, description) 
VALUES 
('scraping_interval', '20', 'Minutes between scraping runs'),
('max_posts_per_run', '50', 'Maximum posts to scrape per run'),
('email_notifications', 'true', 'Enable email notifications'),
('default_city', 'Tel Aviv', 'Default city for filtering');

-- Insert sample Facebook groups
INSERT INTO facebook_groups (group_name, group_url, is_active) 
VALUES 
('Tel Aviv Apartments', 'https://facebook.com/groups/telavivapartments', true),
('Jerusalem Rentals', 'https://facebook.com/groups/jerusalemrentals', true),
('Haifa Housing', 'https://facebook.com/groups/haifahousing', true);

-- =====================================================
-- 10. VERIFICATION QUERIES
-- =====================================================

-- Verify all tables were created
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- Count records in each table
SELECT 
    'properties' as table_name, COUNT(*) as record_count FROM properties
UNION ALL
SELECT 
    'posts' as table_name, COUNT(*) as record_count FROM posts
UNION ALL
SELECT 
    'schedules' as table_name, COUNT(*) as record_count FROM schedules
UNION ALL
SELECT 
    'scraping_logs' as table_name, COUNT(*) as record_count FROM scraping_logs
UNION ALL
SELECT 
    'email_notifications' as table_name, COUNT(*) as record_count FROM email_notifications
UNION ALL
SELECT 
    'user_settings' as table_name, COUNT(*) as record_count FROM user_settings
UNION ALL
SELECT 
    'facebook_groups' as table_name, COUNT(*) as record_count FROM facebook_groups;

-- =====================================================
-- SETUP COMPLETE!
-- =====================================================
-- Your Supabase database is now ready with all required tables
-- You can now run your Flask application and it should work perfectly!
