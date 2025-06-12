import sqlite3
import os
from datetime import datetime

def debug_vendor_status():
    """Debug vendor registration status"""
    # Check if database exists
    db_path = 'instance/mypevo.db'
    if not os.path.exists(db_path):
        print(f"Database not found at: {db_path}")
        print("Current directory:", os.getcwd())
        print("Files in current directory:")
        for f in os.listdir('.'):
            print(f"  {f}")
        if os.path.exists('instance'):
            print("Files in instance directory:")
            for f in os.listdir('instance'):
                print(f"  {f}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("=== VENDOR USERS ===")
        cursor.execute("SELECT id, company_name, email, user_type, is_approved FROM user WHERE user_type = 'vendor'")
        vendors = cursor.fetchall()
        
        if vendors:
            for vendor in vendors:
                print(f"Vendor ID: {vendor[0]}, Company: {vendor[1]}, Email: {vendor[2]}, Type: {vendor[3]}, Approved: {vendor[4]}")
                
                # Check vendor locations for this vendor
                cursor.execute("SELECT id, company_name, is_registered_vendor, expires_at FROM vendor_location WHERE user_id = ?", (vendor[0],))
                locations = cursor.fetchall()
                
                print(f"  Locations shared: {len(locations)}")
                for location in locations:
                    expires_at_str = location[3]
                    try:
                        # Try different datetime formats
                        if 'T' in expires_at_str:
                            expires_at = datetime.fromisoformat(expires_at_str.replace('Z', '+00:00'))
                        else:
                            expires_at = datetime.strptime(expires_at_str, '%Y-%m-%d %H:%M:%S')
                        is_active = expires_at > datetime.utcnow()
                    except:
                        is_active = "Unknown"
                    print(f"    Location ID: {location[0]}, Company: {location[1]}, Registered: {location[2]}, Active: {is_active}")
        else:
            print("No vendor users found")
        
        print("\n=== ALL VENDOR LOCATIONS ===")
        cursor.execute("SELECT id, company_name, user_id, is_registered_vendor, expires_at FROM vendor_location ORDER BY created_at DESC")
        all_locations = cursor.fetchall()
        
        if all_locations:
            for location in all_locations:
                user_id = location[2]
                if user_id:
                    cursor.execute("SELECT company_name, user_type FROM user WHERE id = ?", (user_id,))
                    user_info = cursor.fetchone()
                    user_display = f"{user_info[0]} ({user_info[1]})" if user_info else "User not found"
                else:
                    user_display = "Guest"
                    
                expires_at_str = location[4]
                try:
                    if 'T' in expires_at_str:
                        expires_at = datetime.fromisoformat(expires_at_str.replace('Z', '+00:00'))
                    else:
                        expires_at = datetime.strptime(expires_at_str, '%Y-%m-%d %H:%M:%S')
                    is_active = expires_at > datetime.utcnow()
                except:
                    is_active = "Unknown"
                
                print(f"Location ID: {location[0]}")
                print(f"  Company: {location[1]}")
                print(f"  User: {user_display}")
                print(f"  Registered: {location[3]}")
                print(f"  Active: {is_active}")
                print()
        else:
            print("No vendor locations found")
            
        # Check all users
        print("\n=== ALL USERS ===")
        cursor.execute("SELECT id, company_name, email, user_type, is_approved, is_admin FROM user ORDER BY created_at DESC")
        all_users = cursor.fetchall()
        
        for user in all_users:
            print(f"User ID: {user[0]}, Company: {user[1]}, Email: {user[2]}, Type: {user[3]}, Approved: {user[4]}, Admin: {user[5]}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_vendor_status() 