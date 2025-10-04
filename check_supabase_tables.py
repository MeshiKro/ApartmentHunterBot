#!/usr/bin/env python3
"""
Check what tables exist in Supabase and create the properties table if needed
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def check_tables():
    """Check what tables exist in Supabase"""
    base_url = "https://qijcswttgyypxrlfzmcv.supabase.co"
    api_key = os.getenv("SUPABASE_ANON_KEY")
    
    headers = {
        "apikey": api_key,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Try to get information about existing tables
    print("🔍 Checking existing tables...")
    
    # Try different common table names
    table_names = ["properties", "posts", "apartments", "listings"]
    
    for table_name in table_names:
        try:
            url = f"{base_url}/rest/v1/{table_name}"
            response = requests.get(url, headers=headers, params={"select": "*", "limit": 1}, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Table '{table_name}' exists")
                data = response.json()
                if data:
                    print(f"   Sample columns: {list(data[0].keys())}")
                else:
                    print(f"   Table is empty")
            elif response.status_code == 404:
                print(f"❌ Table '{table_name}' does not exist")
            else:
                print(f"⚠️  Table '{table_name}' - Status: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error checking table '{table_name}': {e}")
    
    print("\n" + "="*50)
    
    # Try to get schema information
    try:
        print("🔍 Checking database schema...")
        url = f"{base_url}/rest/v1/"
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Root endpoint status: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
    except Exception as e:
        print(f"Error checking schema: {e}")

if __name__ == "__main__":
    check_tables()
