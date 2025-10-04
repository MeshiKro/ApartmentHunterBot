"""
Complete Supabase REST API Client for Apartment Hunter Bot
Supports all database tables and operations
"""
import os
import requests
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv
import logging
from datetime import datetime

load_dotenv()

class CompleteSupabaseClient:
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
            return response.status_code in [200, 404]
        except Exception as e:
            logging.error(f"Supabase connection test failed: {e}")
            return False
    
    # =====================================================
    # PROPERTIES TABLE OPERATIONS
    # =====================================================
    
    def get_properties(self, limit: int = 100, order_by: str = "created_at.desc", filters: Dict = None) -> List[Dict]:
        """Get properties from the database"""
        try:
            url = f"{self.base_url}/rest/v1/properties"
            params = {
                "select": "*", 
                "order": order_by, 
                "limit": limit
            }
            
            if filters:
                for key, value in filters.items():
                    params[key] = f"eq.{value}"
            
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
    
    # =====================================================
    # POSTS TABLE OPERATIONS
    # =====================================================
    
    def get_posts(self, limit: int = 100, order_by: str = "created_at.desc") -> List[Dict]:
        """Get posts from the database"""
        try:
            url = f"{self.base_url}/rest/v1/posts"
            params = {
                "select": "*", 
                "order": order_by, 
                "limit": limit
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            logging.error(f"Failed to get posts: {e}")
            return []
    
    def insert_post(self, post_data: Dict) -> bool:
        """Insert a new post"""
        try:
            url = f"{self.base_url}/rest/v1/posts"
            response = requests.post(url, headers=self.headers, json=post_data, timeout=30)
            response.raise_for_status()
            return True
        except Exception as e:
            logging.error(f"Failed to insert post: {e}")
            return False
    
    def insert_posts_bulk(self, posts: List[Dict]) -> bool:
        """Insert multiple posts at once"""
        try:
            url = f"{self.base_url}/rest/v1/posts"
            response = requests.post(url, headers=self.headers, json=posts, timeout=60)
            response.raise_for_status()
            return True
        except Exception as e:
            logging.error(f"Failed to insert posts bulk: {e}")
            return False
    
    # =====================================================
    # SCHEDULES TABLE OPERATIONS
    # =====================================================
    
    def get_schedules(self, active_only: bool = True) -> List[Dict]:
        """Get schedules from the database"""
        try:
            url = f"{self.base_url}/rest/v1/schedules"
            params = {"select": "*", "order": "created_at.desc"}
            
            if active_only:
                params["is_active"] = "eq.true"
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            logging.error(f"Failed to get schedules: {e}")
            return []
    
    def save_schedule(self, schedule_data: Dict) -> bool:
        """Save or update a schedule"""
        try:
            # Check if schedule exists
            existing = self.get_schedules(active_only=False)
            
            if existing:
                # Update existing schedule
                schedule_id = existing[0]['id']
                url = f"{self.base_url}/rest/v1/schedules"
                params = {"id": f"eq.{schedule_id}"}
                response = requests.patch(url, headers=self.headers, params=params, json=schedule_data, timeout=30)
            else:
                # Insert new schedule
                url = f"{self.base_url}/rest/v1/schedules"
                response = requests.post(url, headers=self.headers, json=schedule_data, timeout=30)
            
            response.raise_for_status()
            return True
        except Exception as e:
            logging.error(f"Failed to save schedule: {e}")
            return False
    
    # =====================================================
    # SCRAPING LOGS TABLE OPERATIONS
    # =====================================================
    
    def create_scraping_log(self, run_id: str, start_time: str = None) -> bool:
        """Create a new scraping log entry"""
        try:
            url = f"{self.base_url}/rest/v1/scraping_logs"
            log_data = {
                "run_id": run_id,
                "start_time": start_time or datetime.now().isoformat(),
                "status": "running"
            }
            
            response = requests.post(url, headers=self.headers, json=log_data, timeout=30)
            response.raise_for_status()
            return True
        except Exception as e:
            logging.error(f"Failed to create scraping log: {e}")
            return False
    
    def update_scraping_log(self, run_id: str, updates: Dict) -> bool:
        """Update a scraping log entry"""
        try:
            url = f"{self.base_url}/rest/v1/scraping_logs"
            params = {"run_id": f"eq.{run_id}"}
            response = requests.patch(url, headers=self.headers, params=params, json=updates, timeout=30)
            response.raise_for_status()
            return True
        except Exception as e:
            logging.error(f"Failed to update scraping log: {e}")
            return False
    
    def get_scraping_logs(self, limit: int = 50) -> List[Dict]:
        """Get scraping logs"""
        try:
            url = f"{self.base_url}/rest/v1/scraping_logs"
            params = {
                "select": "*", 
                "order": "created_at.desc", 
                "limit": limit
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            logging.error(f"Failed to get scraping logs: {e}")
            return []
    
    # =====================================================
    # EMAIL NOTIFICATIONS TABLE OPERATIONS
    # =====================================================
    
    def log_email_notification(self, recipient_email: str, subject: str, posts_count: int) -> bool:
        """Log an email notification"""
        try:
            url = f"{self.base_url}/rest/v1/email_notifications"
            notification_data = {
                "recipient_email": recipient_email,
                "subject": subject,
                "posts_count": posts_count,
                "status": "sent"
            }
            
            response = requests.post(url, headers=self.headers, json=notification_data, timeout=30)
            response.raise_for_status()
            return True
        except Exception as e:
            logging.error(f"Failed to log email notification: {e}")
            return False
    
    def get_email_notifications(self, limit: int = 50) -> List[Dict]:
        """Get email notifications"""
        try:
            url = f"{self.base_url}/rest/v1/email_notifications"
            params = {
                "select": "*", 
                "order": "sent_at.desc", 
                "limit": limit
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            logging.error(f"Failed to get email notifications: {e}")
            return []
    
    # =====================================================
    # USER SETTINGS TABLE OPERATIONS
    # =====================================================
    
    def get_setting(self, setting_key: str) -> Optional[str]:
        """Get a user setting value"""
        try:
            url = f"{self.base_url}/rest/v1/user_settings"
            params = {
                "select": "setting_value",
                "setting_key": f"eq.{setting_key}"
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return data[0]['setting_value'] if data else None
        except Exception as e:
            logging.error(f"Failed to get setting {setting_key}: {e}")
            return None
    
    def set_setting(self, setting_key: str, setting_value: str, description: str = None) -> bool:
        """Set a user setting value"""
        try:
            # Check if setting exists
            url = f"{self.base_url}/rest/v1/user_settings"
            params = {"setting_key": f"eq.{setting_key}"}
            
            # Try to update first
            update_data = {"setting_value": setting_value}
            if description:
                update_data["description"] = description
            
            response = requests.patch(url, headers=self.headers, params=params, json=update_data, timeout=30)
            
            if response.status_code == 200:
                return True
            
            # If update failed, insert new setting
            setting_data = {
                "setting_key": setting_key,
                "setting_value": setting_value,
                "description": description or f"Setting for {setting_key}"
            }
            
            response = requests.post(url, headers=self.headers, json=setting_data, timeout=30)
            response.raise_for_status()
            return True
        except Exception as e:
            logging.error(f"Failed to set setting {setting_key}: {e}")
            return False
    
    # =====================================================
    # FACEBOOK GROUPS TABLE OPERATIONS
    # =====================================================
    
    def get_facebook_groups(self, active_only: bool = True) -> List[Dict]:
        """Get Facebook groups"""
        try:
            url = f"{self.base_url}/rest/v1/facebook_groups"
            params = {"select": "*", "order": "created_at.desc"}
            
            if active_only:
                params["is_active"] = "eq.true"
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            logging.error(f"Failed to get Facebook groups: {e}")
            return []
    
    def add_facebook_group(self, group_name: str, group_url: str) -> bool:
        """Add a new Facebook group"""
        try:
            url = f"{self.base_url}/rest/v1/facebook_groups"
            group_data = {
                "group_name": group_name,
                "group_url": group_url,
                "is_active": True
            }
            
            response = requests.post(url, headers=self.headers, json=group_data, timeout=30)
            response.raise_for_status()
            return True
        except Exception as e:
            logging.error(f"Failed to add Facebook group: {e}")
            return False
    
    def update_facebook_group(self, group_id: int, updates: Dict) -> bool:
        """Update a Facebook group"""
        try:
            url = f"{self.base_url}/rest/v1/facebook_groups"
            params = {"id": f"eq.{group_id}"}
            response = requests.patch(url, headers=self.headers, params=params, json=updates, timeout=30)
            response.raise_for_status()
            return True
        except Exception as e:
            logging.error(f"Failed to update Facebook group: {e}")
            return False

# Global instance
supabase_client = CompleteSupabaseClient()
