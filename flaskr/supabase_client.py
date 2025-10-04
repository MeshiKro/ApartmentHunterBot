"""
Supabase REST API Client for Flask App
Replaces direct PostgreSQL connections with Supabase REST API
"""
import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv
import logging
from datetime import datetime

load_dotenv()

class SupabaseClient:
    def __init__(self):
        self.base_url = os.getenv("SUPABASE_URL", "https://qijcswttgyypxrlfzmcv.supabase.co")
        self.api_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not self.api_key:
            raise ValueError("SUPABASE_ANON_KEY not found in environment variables")
        
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
    
    def get_properties(self, limit: int = 100, order_by: str = "created_at.desc") -> List[Dict]:
        """Get properties from the database"""
        try:
            url = f"{self.base_url}/rest/v1/properties"
            params = {
                "select": "*", 
                "order": order_by, 
                "limit": limit
            }
            
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
    
    def get_property_by_id(self, property_id: int) -> Optional[Dict]:
        """Get a single property by ID"""
        try:
            url = f"{self.base_url}/rest/v1/properties"
            params = {"id": f"eq.{property_id}", "select": "*"}
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            
            results = response.json()
            return results[0] if results else None
        except Exception as e:
            logging.error(f"Failed to get property by ID: {e}")
            return None

# Global instance
supabase_client = SupabaseClient()
