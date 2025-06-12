import sqlite3

def check_database():
    conn = sqlite3.connect('instance/mypevo.db')
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("Tables:", [t[0] for t in tables])
    
    # Check user table structure
    cursor.execute("PRAGMA table_info(user)")
    columns = cursor.fetchall()
    print("\nUser table columns:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    conn.close()

if __name__ == "__main__":
    check_database() 