"""
Supabase REST API Client for Apartment Hunter Bot
This replaces direct PostgreSQL connections with Supabase REST API calls
"""
import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv
import logging

load_dotenv()

class SupabaseClient:
    def __init__(self):
        self.base_url = "https://qijcswttgyypxrlfzmcv.supabase.co"
        self.api_key = os.getenv("SUPABASE_ANON_KEY")  # You'll need to add this to .env
        self.headers = {
            "apikey": self.api_key,
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        
    def test_connection(self) -> bool:
        """Test if Supabase API is accessible"""
        try:
            response = requests.get(f"{self.base_url}/rest/v1/", headers=self.headers, timeout=10)
            return response.status_code in [200, 404]  # 404 is OK for root endpoint
        except Exception as e:
            logging.error(f"Supabase connection test failed: {e}")
            return False
    
    def get_properties(self, limit: int = 100) -> List[Dict]:
        """Get properties from the database"""
        try:
            url = f"{self.base_url}/rest/v1/properties"
            params = {"select": "*", "order": "created_at.desc", "limit": limit}
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            logging.error(f"Failed to get properties: {e}")
            return []
    
    def insert_property(self, property_data: Dict) -> bool:
        """Insert a new property"""
        try:
            url = f"{self.base_url}/rest/v1/properties"
            
            response = requests.post(url, headers=self.headers, json=property_data, timeout=30)
            response.raise_for_status()
            
            return True
        except Exception as e:
            logging.error(f"Failed to insert property: {e}")
            return False
    
    def insert_properties_bulk(self, properties: List[Dict]) -> bool:
        """Insert multiple properties at once"""
        try:
            url = f"{self.base_url}/rest/v1/properties"
            
            response = requests.post(url, headers=self.headers, json=properties, timeout=60)
            response.raise_for_status()
            
            return True
        except Exception as e:
            logging.error(f"Failed to insert properties bulk: {e}")
            return False
    
    def update_property(self, property_id: int, updates: Dict) -> bool:
        """Update a property by ID"""
        try:
            url = f"{self.base_url}/rest/v1/properties"
            params = {"id": f"eq.{property_id}"}
            
            response = requests.patch(url, headers=self.headers, params=params, json=updates, timeout=30)
            response.raise_for_status()
            
            return True
        except Exception as e:
            logging.error(f"Failed to update property: {e}")
            return False

# Example usage
if __name__ == "__main__":
    client = SupabaseClient()
    
    # Test connection
    if client.test_connection():
        print("✅ Supabase REST API connection successful!")
        
        # Get properties
        properties = client.get_properties(limit=5)
        print(f"Found {len(properties)} properties")
        
        for prop in properties:
            print(f"- {prop.get('description', 'No description')[:50]}...")
    else:
        print("❌ Supabase REST API connection failed!")
