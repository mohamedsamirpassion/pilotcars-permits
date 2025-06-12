import sqlite3
import os
from datetime import datetime

def migrate_database():
    """Migrate existing database to add new columns for vendor functionality"""
    db_path = 'instance/mypevo.db'
    
    if not os.path.exists(db_path):
        print("Database doesn't exist yet. Run the app to create it.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("Starting database migration...")
        
        # Check current schema
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        print(f"Current user table columns: {columns}")
        
        # Add missing columns to user table
        migrations = []
        
        if 'user_type' not in columns:
            migrations.append("ALTER TABLE user ADD COLUMN user_type VARCHAR(20) DEFAULT 'trucking_company'")
            
        if 'is_approved' not in columns:
            migrations.append("ALTER TABLE user ADD COLUMN is_approved BOOLEAN DEFAULT 0")
            
        if 'is_suspended' not in columns:
            migrations.append("ALTER TABLE user ADD COLUMN is_suspended BOOLEAN DEFAULT 0")
            
        if 'phone_number' not in columns:
            migrations.append("ALTER TABLE user ADD COLUMN phone_number VARCHAR(20)")
        
        # Execute migrations
        for migration in migrations:
            print(f"Executing: {migration}")
            cursor.execute(migration)
        
        # Update existing users
        if migrations:
            print("Updating existing users...")
            
            # Set existing users as trucking companies and approved (except admin)
            cursor.execute("""
                UPDATE user 
                SET user_type = 'trucking_company', 
                    is_approved = 1, 
                    is_suspended = 0 
                WHERE user_type IS NULL OR user_type = ''
            """)
            
            # Admin users should also be approved
            cursor.execute("""
                UPDATE user 
                SET is_approved = 1, 
                    is_suspended = 0 
                WHERE is_admin = 1
            """)
        
        # Check if vendor_location table exists, if not create it
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vendor_location'")
        if not cursor.fetchone():
            print("Creating vendor_location table...")
            cursor.execute("""
                CREATE TABLE vendor_location (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    company_name VARCHAR(100) NOT NULL,
                    contact_name VARCHAR(100),
                    email VARCHAR(120) NOT NULL,
                    phone VARCHAR(20) NOT NULL,
                    location_city VARCHAR(100) NOT NULL,
                    location_state VARCHAR(50) NOT NULL,
                    latitude FLOAT,
                    longitude FLOAT,
                    coverage_radius INTEGER DEFAULT 100,
                    services_provided TEXT NOT NULL,
                    notes TEXT,
                    is_registered_vendor BOOLEAN DEFAULT 0,
                    expires_at DATETIME NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user (id)
                )
            """)
        
        conn.commit()
        print("Database migration completed successfully!")
        
        # Display updated schema
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        print(f"Updated user table columns: {columns}")
        
    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
        
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database() 