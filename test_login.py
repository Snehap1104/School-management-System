"""
Test script to verify login functionality
"""
import requests
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask
from config import Config
from database import init_db, get_db

def test_login():
    """Test login functionality"""
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app)
    
    with app.app_context():
        try:
            cursor = get_db()
            
            # Check admin user
            cursor.execute("SELECT * FROM users WHERE username = 'admin'")
            user = cursor.fetchone()
            
            if not user:
                print("[ERROR] Admin user not found!")
                print("Run: py init_db.py")
                return False
            
            print("\n[OK] Admin user found:")
            print(f"  Username: {user[1]}")
            print(f"  Role: {user[4]}")
            print(f"  Active: {user[5]}")
            
            # Test password
            test_password = 'admin123'
            password_hash = user[3]
            
            if check_password_hash(password_hash, test_password):
                print(f"\n[OK] Password '{test_password}' is CORRECT!")
                print("\nLogin credentials:")
                print(f"  Username: admin")
                print(f"  Password: admin123")
                print("\n[INFO] Try logging in with these credentials at http://localhost:5000")
                return True
            else:
                print(f"\n[ERROR] Password '{test_password}' is INCORRECT!")
                print("Run: py init_db.py to reset password")
                return False
                
        except Exception as e:
            print(f"\n[ERROR] Database error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    print("=" * 60)
    print("LOGIN TEST - Verify Login Credentials")
    print("=" * 60)
    test_login()
    print("\n" + "=" * 60)
    print("\nNext steps:")
    print("1. Make sure app is running: py app.py")
    print("2. Open browser: http://localhost:5000")
    print("3. Login with: admin / admin123")
    print("=" * 60)
