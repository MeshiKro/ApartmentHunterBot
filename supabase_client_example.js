// Corrected Supabase Client Implementation
// This replaces your current connection code

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
    console.log('🔍 Testing Supabase connection...')
    
    // First, test basic connectivity
    const { data: healthCheck, error: healthError } = await supabase
      .from('_health_check')  // This is a built-in table for health checks
      .select('*')
      .limit(1)
    
    if (healthError && healthError.code === 'PGRST116') {
      // Table doesn't exist, but connection is working
      console.log('✅ Supabase connection is working (health check table not found, which is normal)')
      return true
    }
    
    // Test with a real table if health check fails
    const { data, error } = await supabase
      .from('properties')  // Replace with your actual table name
      .select('*')
      .limit(1)
    
    if (error) {
      console.error('❌ Connection failed:', error.message)
      console.error('Error details:', error)
      return false
    } else {
      console.log('✅ Connection successful!')
      console.log('Sample data:', data)
      return true
    }
  } catch (err) {
    console.error('❌ Unexpected error:', err)
    return false
  }
}

// Database operations examples
class SupabaseDatabase {
  constructor() {
    this.client = supabase
  }

  // Insert data
  async insertData(tableName, data) {
    try {
      const { data: result, error } = await this.client
        .from(tableName)
        .insert(data)
        .select()
      
      if (error) throw error
      return { success: true, data: result }
    } catch (error) {
      console.error('Insert error:', error)
      return { success: false, error: error.message }
    }
  }

  // Select data
  async selectData(tableName, filters = {}) {
    try {
      let query = this.client.from(tableName).select('*')
      
      // Apply filters
      Object.entries(filters).forEach(([key, value]) => {
        query = query.eq(key, value)
      })
      
      const { data, error } = await query
      
      if (error) throw error
      return { success: true, data }
    } catch (error) {
      console.error('Select error:', error)
      return { success: false, error: error.message }
    }
  }

  // Update data
  async updateData(tableName, id, updates) {
    try {
      const { data, error } = await this.client
        .from(tableName)
        .update(updates)
        .eq('id', id)
        .select()
      
      if (error) throw error
      return { success: true, data }
    } catch (error) {
      console.error('Update error:', error)
      return { success: false, error: error.message }
    }
  }

  // Delete data
  async deleteData(tableName, id) {
    try {
      const { error } = await this.client
        .from(tableName)
        .delete()
        .eq('id', id)
      
      if (error) throw error
      return { success: true }
    } catch (error) {
      console.error('Delete error:', error)
      return { success: false, error: error.message }
    }
  }
}

// Usage example
async function main() {
  console.log('🚀 Starting Supabase connection test...')
  
  // Test connection
  const connectionOk = await testSupabaseConnection()
  
  if (connectionOk) {
    console.log('✅ Ready to use Supabase!')
    
    // Example usage
    const db = new SupabaseDatabase()
    
    // Example: Insert a property
    const propertyData = {
      title: 'Test Property',
      price: 1500,
      location: 'Test City',
      description: 'Test description'
    }
    
    const insertResult = await db.insertData('properties', propertyData)
    console.log('Insert result:', insertResult)
    
    // Example: Select properties
    const selectResult = await db.selectData('properties', { price: 1500 })
    console.log('Select result:', selectResult)
    
  } else {
    console.log('❌ Connection failed. Please check your configuration.')
  }
}

// Export for use in your application
export { supabase, testSupabaseConnection, SupabaseDatabase }

// Run if this file is executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error)
}
