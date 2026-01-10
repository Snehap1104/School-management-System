"""
Script to check login issues and verify database setup
"""
from flask import Flask
from config import Config
from database import init_db, get_db
from werkzeug.security import check_password_hash

def check_database():
    """Check database and admin user"""
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app)
    
    with app.app_context():
        try:
            cursor = get_db()
            
            # Check if admin user exists
            cursor.execute("SELECT id, username, email, password_hash, role, is_active FROM users WHERE username = 'admin'")
            admin = cursor.fetchone()
            
            if admin:
                print("\n[OK] Admin user found in database:")
                print(f"  ID: {admin[0]}")
                print(f"  Username: {admin[1]}")
                print(f"  Email: {admin[2]}")
                print(f"  Role: {admin[4]}")
                print(f"  Active: {admin[5]}")
                print(f"  Password Hash: {admin[3][:50]}...")
                
                # Test password
                test_password = 'admin123'
                if check_password_hash(admin[3], test_password):
                    print(f"\n[OK] Password 'admin123' is CORRECT!")
                    print("  Login should work with: admin / admin123")
                else:
                    print(f"\n[ERROR] Password 'admin123' is INCORRECT!")
                    print("  Run: py init_db.py to reset password")
                
            else:
                print("\n[ERROR] Admin user NOT found in database!")
                print("  Run: py init_db.py to create admin user")
                
            # Check if users table exists
            cursor.execute("SHOW TABLES LIKE 'users'")
            if cursor.fetchone():
                print("\n[OK] Users table exists")
            else:
                print("\n[ERROR] Users table does not exist!")
                print("  Run: mysql -u root -p school_management < database.sql")
                
            # Count users
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            print(f"\n[INFO] Total users in database: {count}")
            
        except Exception as e:
            print(f"\n[ERROR] Database error: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    print("=" * 60)
    print("LOGIN CHECK - Database Verification")
    print("=" * 60)
    check_database()
    print("\n" + "=" * 60)
