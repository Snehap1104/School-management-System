"""
Script to create a teacher user for testing
"""
from werkzeug.security import generate_password_hash
from flask import Flask
from config import Config
from database import init_db, get_db
from datetime import date

def create_teacher():
    """Create a teacher user"""
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app)
    
    with app.app_context():
        try:
            cursor = get_db()
            
            # Teacher details
            username = 'teacher'
            password = 'teacher123'
            email = 'teacher@school.com'
            first_name = 'John'
            last_name = 'Smith'
            employee_id = 'EMP001'
            
            # Check if teacher user already exists
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                print(f"[INFO] User '{username}' already exists!")
                print("Updating password...")
                password_hash = generate_password_hash(password)
                cursor.execute(
                    "UPDATE users SET password_hash = %s WHERE username = %s",
                    (password_hash, username)
                )
                cursor.connection.commit()
                print(f"[OK] Password updated for user '{username}'")
            else:
                # Create user account
                password_hash = generate_password_hash(password)
                cursor.execute(
                    "INSERT INTO users (username, email, password_hash, role, is_active) VALUES (%s, %s, %s, %s, %s)",
                    (username, email, password_hash, 'teacher', True)
                )
                user_id = cursor.lastrowid
                
                # Create teacher record
                cursor.execute("""
                    INSERT INTO teachers 
                    (user_id, first_name, last_name, employee_id, phone, qualification, specialization, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (user_id, first_name, last_name, employee_id, '1234567890', 'M.Sc., B.Ed.', 'Mathematics', True))
                
                cursor.connection.commit()
                print(f"[OK] Teacher user created successfully!")
            
            print("\n" + "=" * 60)
            print("TEACHER LOGIN CREDENTIALS:")
            print("=" * 60)
            print(f"Username: {username}")
            print(f"Password: {password}")
            print(f"Email: {email}")
            print(f"Name: {first_name} {last_name}")
            print(f"Employee ID: {employee_id}")
            print("=" * 60)
            print("\n[INFO] You can now login with these credentials at http://localhost:5000")
            print("\nTeacher Features:")
            print("  - Upload study notes")
            print("  - Mark attendance")
            print("  - View students")
            print("  - View assigned classes and subjects")
            
            return True
            
        except Exception as e:
            print(f"\n[ERROR] Error creating teacher: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    print("=" * 60)
    print("CREATE TEACHER USER")
    print("=" * 60)
    create_teacher()
    print("\n" + "=" * 60)
