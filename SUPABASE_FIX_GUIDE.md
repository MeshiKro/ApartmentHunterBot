# Supabase Connection Fix Guide

## Problem Analysis
Your Supabase connection is consistently timing out with the error:
```
connection to server at "qijcswttgyypxrlfzmcv.supabase.co" failed: timeout expired
```

## Root Causes
1. **Supabase Project Status**: Your project might be paused or inactive
2. **Network/Firewall Issues**: Port 5432 might be blocked
3. **Incorrect Connection Method**: Direct PostgreSQL connection might not be the best approach
4. **Missing Environment Variables**: SUPABASE_KEY not properly configured

## Solutions

### 1. Check Supabase Project Status
**IMMEDIATE ACTION REQUIRED:**
1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Navigate to your project: `qijcswttgyypxrlfzmcv`
3. Check if the project is:
   - ✅ Active and running
   - ❌ Paused (common on free tier)
   - ❌ Suspended due to usage limits

**If paused:** Click "Resume" or "Restore" to reactivate your project.

### 2. Fix Your JavaScript Code
Replace your current code with this corrected version:

```javascript
import { createClient } from '@supabase/supabase-js'

// Your Supabase project details
const supabaseUrl = 'https://qijcswttgyypxrlfzmcv.supabase.co'
const supabaseKey = process.env.SUPABASE_ANON_KEY  // Use anon key, not service role

// Create the client with proper configuration
const supabase = createClient(supabaseUrl, supabaseKey, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true
  },
  db: {
    schema: 'public'
  },
  global: {
    headers: {
      'X-Client-Info': 'apartment-hunter-bot'
    }
  }
})

// Test connection function
async function testSupabaseConnection() {
  try {
    console.log('Testing Supabase connection...')
    
    // Test with a simple query
    const { data, error } = await supabase
      .from('your_table_name')  // Replace with actual table name
      .select('*')
      .limit(1)
    
    if (error) {
      console.error('❌ Connection failed:', error.message)
      return false
    } else {
      console.log('✅ Connection successful!', data)
      return true
    }
  } catch (err) {
    console.error('❌ Unexpected error:', err)
    return false
  }
}

// Export for use in your application
export { supabase, testSupabaseConnection }
```

### 3. Environment Variables Setup
Create a `.env` file with the correct Supabase keys:

```env
# Supabase Configuration
SUPABASE_URL=https://qijcswttgyypxrlfzmcv.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here

# For Python/Flask (if still needed)
SQLALCHEMY_DATABASE_URI=postgresql://postgres:mozcPp1J13dCzp4N@qijcswttgyypxrlfzmcv.supabase.co:5432/ApartmentHunterBot
POSTGRES_URL=postgresql://postgres:mozcPp1J13dCzp4N@qijcswttgyypxrlfzmcv.supabase.co:5432/ApartmentHunterBot
```

**To get your keys:**
1. Go to Supabase Dashboard → Settings → API
2. Copy the `anon` `public` key for client-side use
3. Copy the `service_role` key for server-side use (keep secret!)

### 4. Alternative: Use Supabase REST API
If direct PostgreSQL connection continues to fail, use the REST API:

```javascript
// Using fetch instead of direct database connection
async function fetchFromSupabase(tableName) {
  const response = await fetch(
    `https://qijcswttgyypxrlfzmcv.supabase.co/rest/v1/${tableName}`,
    {
      headers: {
        'apikey': process.env.SUPABASE_ANON_KEY,
        'Authorization': `Bearer ${process.env.SUPABASE_ANON_KEY}`,
        'Content-Type': 'application/json'
      }
    }
  )
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
  
  return await response.json()
}
```

### 5. Network Troubleshooting
If the issue persists:

1. **Test from different network:**
   ```bash
   # Test basic connectivity
   ping qijcswttgyypxrlfzmcv.supabase.co
   
   # Test port 5432 (if using direct PostgreSQL)
   telnet qijcswttgyypxrlfzmcv.supabase.co 5432
   ```

2. **Check firewall settings:**
   - Ensure port 5432 is not blocked
   - Try using a VPN if on corporate network

3. **Use different connection method:**
   - Switch to Supabase JavaScript client (recommended)
   - Use connection pooling
   - Try different ports if available

### 6. Python/Flask Integration
If you need to keep using Python with Supabase:

```python
import os
from supabase import create_client, Client

# Initialize Supabase client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(url, key)

# Test connection
def test_connection():
    try:
        response = supabase.table('your_table').select("*").limit(1).execute()
        print("✅ Connection successful!")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False
```

## Recommended Action Plan

1. **IMMEDIATE**: Check Supabase dashboard and resume project if paused
2. **SHORT-TERM**: Switch to Supabase JavaScript client instead of direct PostgreSQL
3. **LONG-TERM**: Implement proper error handling and connection retry logic

## Why This Happens
- **Free Tier Limitations**: Supabase free tier pauses projects after inactivity
- **Network Restrictions**: Some networks block direct database connections
- **Security Policies**: Direct PostgreSQL connections are often restricted in production

The Supabase JavaScript client is more reliable because it:
- Uses HTTPS instead of raw TCP connections
- Handles authentication automatically
- Provides better error messages
- Works through firewalls and proxies
