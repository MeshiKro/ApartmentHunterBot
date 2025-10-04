#!/usr/bin/env python3
"""
Test script to diagnose Supabase connection issues
"""
import os
import sys
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine, text
import requests

# Load environment variables
load_dotenv()

def test_supabase_api():
    """Test Supabase REST API connection"""
    print("🔍 Testing Supabase REST API...")
    
    url = "https://qijcswttgyypxrlfzmcv.supabase.co/rest/v1/"
    headers = {
        "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFpamNzd3R0Z3l5cHhybGZ6bWN2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk1MDUxMjksImV4cCI6MjA3NTA4MTEyOX0.VklxpsER8pVretoQ-_D44Rq6S8B-lGYj5Mac0hrhOzc",  # You'll need to add this
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFpamNzd3R0Z3l5cHhybGZ6bWN2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk1MDUxMjksImV4cCI6MjA3NTA4MTEyOX0.VklxpsER8pVretoQ-_D44Rq6S8B-lGYj5Mac0hrhOzc"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"✅ REST API Status: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ REST API Error: {e}")
        return False

def test_postgres_connection():
    """Test direct PostgreSQL connection"""
    print("🔍 Testing PostgreSQL connection...")
    
    connection_string = os.getenv("POSTGRES_URL")
    if not connection_string:
        print("❌ POSTGRES_URL not found in environment")
        return False
    
    print(f"Connection string: {connection_string[:50]}...")
    
    try:
        # Test with psycopg2
        conn = psycopg2.connect(connection_string, connect_timeout=10)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ PostgreSQL connection successful!")
        print(f"Database version: {version[0][:50]}...")
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_sqlalchemy_connection():
    """Test SQLAlchemy connection"""
    print("🔍 Testing SQLAlchemy connection...")
    
    connection_string = os.getenv("SQLALCHEMY_DATABASE_URI")
    if not connection_string:
        print("❌ SQLALCHEMY_DATABASE_URI not found in environment")
        return False
    
    try:
        engine = create_engine(connection_string, connect_args={"connect_timeout": 10})
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            test_value = result.fetchone()[0]
            print(f"✅ SQLAlchemy connection successful! Test value: {test_value}")
        return True
        
    except Exception as e:
        print(f"❌ SQLAlchemy connection failed: {e}")
        return False

def main():
    print("=" * 60)
    print("SUPABASE CONNECTION DIAGNOSTIC TOOL")
    print("=" * 60)
    
    # Test 1: REST API
    api_success = test_supabase_api()
    print()
    
    # Test 2: Direct PostgreSQL
    pg_success = test_postgres_connection()
    print()
    
    # Test 3: SQLAlchemy
    sa_success = test_sqlalchemy_connection()
    print()
    
    print("=" * 60)
    print("SUMMARY:")
    print(f"REST API: {'✅ Working' if api_success else '❌ Failed'}")
    print(f"PostgreSQL: {'✅ Working' if pg_success else '❌ Failed'}")
    print(f"SQLAlchemy: {'✅ Working' if sa_success else '❌ Failed'}")
    
    if not any([api_success, pg_success, sa_success]):
        print("\n🚨 ALL CONNECTIONS FAILED!")
        print("Possible causes:")
        print("1. Supabase project is paused/inactive")
        print("2. IP address is banned")
        print("3. Network/firewall blocking port 5432")
        print("4. Incorrect credentials")
        print("\nNext steps:")
        print("1. Check Supabase Dashboard for project status")
        print("2. Unban your IP if necessary")
        print("3. Consider using Supabase REST API instead of direct PostgreSQL")

if __name__ == "__main__":
    main()
