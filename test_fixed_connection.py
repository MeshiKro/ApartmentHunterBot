#!/usr/bin/env python3
"""
Test the fixed Supabase connection after creating the properties table
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_properties_table():
    """Test if the properties table is now accessible"""
    base_url = "https://qijcswttgyypxrlfzmcv.supabase.co"
    api_key = os.getenv("SUPABASE_ANON_KEY")
    
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print("🔍 Testing properties table access...")
    
    try:
        # Test GET request
        url = f"{base_url}/rest/v1/properties"
        response = requests.get(url, headers=headers, params={"select": "*", "limit": 5}, timeout=10)
        
        if response.status_code == 200:
            print("✅ Properties table is accessible!")
            data = response.json()
            print(f"Found {len(data)} properties:")
            
            for i, prop in enumerate(data, 1):
                print(f"  {i}. {prop.get('description', 'No description')[:50]}...")
                print(f"     Price: {prop.get('price')}, Rooms: {prop.get('rooms')}, City: {prop.get('city')}")
            
            return True
        else:
            print(f"❌ Cannot access properties table. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing table access: {e}")
        return False

def test_insert_property():
    """Test inserting a new property"""
    base_url = "https://qijcswttgyypxrlfzmcv.supabase.co"
    api_key = os.getenv("SUPABASE_ANON_KEY")
    
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    print("📝 Testing property insertion...")
    
    test_property = {
        "description": "Test apartment from Python script",
        "address": "Test Street 123",
        "price": 10000.00,
        "rooms": 2,
        "size": 70.0,
        "phone": "+972-50-999-8888",
        "city": "Test City",
        "url": "https://example.com/test",
        "sent": False
    }
    
    try:
        url = f"{base_url}/rest/v1/properties"
        response = requests.post(url, headers=headers, json=test_property, timeout=30)
        
        if response.status_code in [200, 201]:
            print("✅ Property insertion successful!")
            return True
        else:
            print(f"❌ Failed to insert property. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error inserting property: {e}")
        return False

def main():
    print("=" * 60)
    print("TESTING FIXED SUPABASE CONNECTION")
    print("=" * 60)
    
    # Test 1: Check if table exists and is accessible
    if test_properties_table():
        print()
        
        # Test 2: Test inserting data
        test_insert_property()
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
