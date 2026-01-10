"""
Database initialization script
Run this script to set up the database with proper admin password hash
"""
from werkzeug.security import generate_password_hash
from flask import Flask
from config import Config
from database import init_db, get_db

def init_database():
    """Initialize database with admin user"""
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app)
    
    with app.app_context():
        try:
            cursor = get_db()
            
            # Generate password hash for admin
            admin_password = 'admin123'
            password_hash = generate_password_hash(admin_password)
            
            # Check if admin exists
            cursor.execute("SELECT id FROM users WHERE username = 'admin'")
            admin = cursor.fetchone()
            
            if admin:
                # Update admin password
                cursor.execute(
                    "UPDATE users SET password_hash = %s WHERE username = 'admin'",
                    (password_hash,)
                )
                print("[OK] Admin password updated successfully!")
                print(f"  Username: admin")
                print(f"  Password: {admin_password}")
            else:
                # Create admin user
                cursor.execute(
                    "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
                    ('admin', 'admin@school.com', password_hash, 'admin')
                )
                print("[OK] Admin user created successfully!")
                print(f"  Username: admin")
                print(f"  Password: {admin_password}")
            
            cursor.connection.commit()
            print("\n[OK] Database initialized successfully!")
            print("  You can now login with the admin credentials.")
            
        except Exception as e:
            print(f"[ERROR] Error initializing database: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    return True

if __name__ == '__main__':
    print("Initializing School Management System Database...")
    print("-" * 50)
    init_database()
