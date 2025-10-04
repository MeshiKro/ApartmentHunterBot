#!/usr/bin/env python3
"""
Create the properties table in Supabase using SQL
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def create_properties_table():
    """Create the properties table in Supabase"""
    base_url = "https://qijcswttgyypxrlfzmcv.supabase.co"
    api_key = os.getenv("SUPABASE_ANON_KEY")
    
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # SQL to create the properties table
    create_table_sql = """
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
    """
    
    print("🔨 Creating properties table...")
    
    try:
        # Use Supabase's SQL endpoint to execute the CREATE TABLE statement
        url = f"{base_url}/rest/v1/rpc/exec_sql"
        
        payload = {
            "sql": create_table_sql
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            print("✅ Properties table created successfully!")
            return True
        else:
            print(f"❌ Failed to create table. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating table: {e}")
        return False

def test_table_access():
    """Test if we can access the properties table"""
    base_url = "https://qijcswttgyypxrlfzmcv.supabase.co"
    api_key = os.getenv("SUPABASE_ANON_KEY")
    
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print("🔍 Testing table access...")
    
    try:
        url = f"{base_url}/rest/v1/properties"
        response = requests.get(url, headers=headers, params={"select": "*", "limit": 1}, timeout=10)
        
        if response.status_code == 200:
            print("✅ Properties table is accessible!")
            data = response.json()
            print(f"Table structure: {list(data[0].keys()) if data else 'Empty table'}")
            return True
        else:
            print(f"❌ Cannot access properties table. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing table access: {e}")
        return False

def insert_sample_data():
    """Insert sample data to test the table"""
    base_url = "https://qijcswttgyypxrlfzmcv.supabase.co"
    api_key = os.getenv("SUPABASE_ANON_KEY")
    
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    print("📝 Inserting sample data...")
    
    sample_property = {
        "description": "Beautiful 3-bedroom apartment in Tel Aviv",
        "address": "Rothschild Boulevard 1",
        "price": 15000.00,
        "rooms": 3,
        "size": 85.5,
        "phone": "+972-50-123-4567",
        "city": "Tel Aviv",
        "url": "https://example.com/property/1",
        "sent": False
    }
    
    try:
        url = f"{base_url}/rest/v1/properties"
        response = requests.post(url, headers=headers, json=sample_property, timeout=30)
        
        if response.status_code in [200, 201]:
            print("✅ Sample data inserted successfully!")
            return True
        else:
            print(f"❌ Failed to insert sample data. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error inserting sample data: {e}")
        return False

def main():
    print("=" * 60)
    print("SUPABASE TABLE SETUP")
    print("=" * 60)
    
    # Step 1: Create table
    if create_properties_table():
        print()
        
        # Step 2: Test table access
        if test_table_access():
            print()
            
            # Step 3: Insert sample data
            insert_sample_data()
    
    print("\n" + "=" * 60)
    print("SETUP COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
