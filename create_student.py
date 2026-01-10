"""
Script to create a student user for testing
"""
from werkzeug.security import generate_password_hash
from flask import Flask
from config import Config
from database import init_db, get_db
from datetime import date

def create_student():
    """Create a student user"""
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app)
    
    with app.app_context():
        try:
            cursor = get_db()
            
            # Student details
            username = 'student'
            password = 'student123'
            email = 'student@school.com'
            first_name = 'Alice'
            last_name = 'Johnson'
            
            # Get first class and section
            cursor.execute("SELECT id FROM classes LIMIT 1")
            class_result = cursor.fetchone()
            class_id = class_result[0] if class_result else None
            
            cursor.execute("SELECT id FROM sections LIMIT 1")
            section_result = cursor.fetchone()
            section_id = section_result[0] if section_result else None
            
            # Get current academic year
            cursor.execute("SELECT id FROM academic_years WHERE is_current = TRUE LIMIT 1")
            academic_year_result = cursor.fetchone()
            academic_year_id = academic_year_result[0] if academic_year_result else None
            
            # Generate admission number
            year = date.today().year
            cursor.execute("SELECT COUNT(*) FROM students WHERE admission_number LIKE %s", (f'ADM{year}%',))
            count = cursor.fetchone()[0]
            admission_number = f'ADM{year}{str(count + 1).zfill(4)}'
            
            # Check if student user already exists
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
                    (username, email, password_hash, 'student', True)
                )
                user_id = cursor.lastrowid
                
                # Create student record
                cursor.execute("""
                    INSERT INTO students 
                    (user_id, admission_number, first_name, last_name, phone, email, 
                     class_id, section_id, academic_year_id, admission_date, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (user_id, admission_number, first_name, last_name, '9876543210', email,
                      class_id, section_id, academic_year_id, date.today(), True))
                
                cursor.connection.commit()
                print(f"[OK] Student user created successfully!")
            
            print("\n" + "=" * 60)
            print("STUDENT LOGIN CREDENTIALS:")
            print("=" * 60)
            print(f"Username: {username}")
            print(f"Password: {password}")
            print(f"Email: {email}")
            print(f"Name: {first_name} {last_name}")
            print(f"Admission Number: {admission_number}")
            if class_id:
                cursor.execute("SELECT class_name FROM classes WHERE id = %s", (class_id,))
                class_result = cursor.fetchone()
                class_name = class_result[0] if class_result else 'N/A'
                print(f"Class: {class_name}")
            print("=" * 60)
            print("\n[INFO] You can now login with these credentials at http://localhost:5000")
            print("\nStudent Features:")
            print("  - View study notes for their class")
            print("  - Download notes")
            print("  - View attendance reports")
            print("  - View dashboard with statistics")
            
            return True
            
        except Exception as e:
            print(f"\n[ERROR] Error creating student: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    print("=" * 60)
    print("CREATE STUDENT USER")
    print("=" * 60)
    create_student()
    print("\n" + "=" * 60)
