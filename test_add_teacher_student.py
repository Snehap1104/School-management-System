"""
Test script to verify adding teacher and student works
"""
from flask import Flask
from config import Config
from database import init_db, get_db
from werkzeug.security import generate_password_hash

def test_teacher_add():
    """Test adding a teacher"""
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app)
    
    with app.app_context():
        try:
            cursor = get_db()
            
            print("\n[TEST] Testing Teacher Add Functionality...")
            print("-" * 60)
            
            # Test data
            first_name = "Test"
            last_name = "Teacher"
            employee_id = f"TEST{hash(str(first_name + last_name)) % 10000}"
            username = "testteacher001"
            password = "test123"
            email = "testteacher@school.com"
            
            # Check if already exists
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                print(f"[SKIP] User '{username}' already exists")
                return True
            
            cursor.execute("SELECT id FROM teachers WHERE employee_id = %s", (employee_id,))
            if cursor.fetchone():
                print(f"[SKIP] Employee ID '{employee_id}' already exists")
                return True
            
            # Create user account
            password_hash = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO users (username, email, password_hash, role, is_active) VALUES (%s, %s, %s, %s, %s)",
                (username, email, password_hash, 'teacher', True)
            )
            user_id = cursor.lastrowid
            print(f"[OK] User account created: ID {user_id}")
            
            # Create teacher record (without email - it's not in teachers table)
            cursor.execute("""
                INSERT INTO teachers 
                (user_id, first_name, last_name, employee_id, phone, address,
                 qualification, specialization, hire_date, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (user_id, first_name, last_name, employee_id, '1234567890', None,
                  'M.Sc., B.Ed.', 'Mathematics', None, True))
            print(f"[OK] Teacher record created successfully!")
            
            cursor.connection.commit()
            print(f"[SUCCESS] Teacher '{first_name} {last_name}' added successfully!")
            print(f"  Username: {username}")
            print(f"  Employee ID: {employee_id}")
            return True
            
        except Exception as e:
            print(f"\n[ERROR] Error adding teacher: {str(e)}")
            import traceback
            traceback.print_exc()
            cursor.connection.rollback()
            return False

def test_student_add():
    """Test adding a student"""
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app)
    
    with app.app_context():
        try:
            cursor = get_db()
            
            print("\n[TEST] Testing Student Add Functionality...")
            print("-" * 60)
            
            # Test data
            first_name = "Test"
            last_name = "Student"
            
            # Generate admission number
            from datetime import datetime
            year = datetime.now().year
            cursor.execute("SELECT COUNT(*) FROM students WHERE admission_number LIKE %s", (f'ADM{year}%',))
            count = cursor.fetchone()[0]
            admission_number = f'ADM{year}{str(count + 1).zfill(4)}'
            username = admission_number.lower()
            
            # Check if already exists
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                print(f"[SKIP] User '{username}' already exists")
                return True
            
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
            
            print(f"[INFO] Admission Number: {admission_number}")
            print(f"[INFO] Class ID: {class_id}")
            print(f"[INFO] Section ID: {section_id}")
            print(f"[INFO] Academic Year ID: {academic_year_id}")
            
            # Create user account
            password_hash = generate_password_hash(admission_number)
            cursor.execute(
                "INSERT INTO users (username, email, password_hash, role, is_active) VALUES (%s, %s, %s, %s, %s)",
                (username, f'{username}@school.com', password_hash, 'student', True)
            )
            user_id = cursor.lastrowid
            print(f"[OK] User account created: ID {user_id}")
            
            # Create student record
            cursor.execute("""
                INSERT INTO students 
                (user_id, admission_number, first_name, last_name, date_of_birth, gender, 
                 phone, email, address, parent_name, parent_phone, parent_email, 
                 class_id, section_id, academic_year_id, photo_path, admission_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (user_id, admission_number, first_name, last_name, None, None,
                  None, None, None, None, None, None, 
                  class_id, section_id, academic_year_id, None, datetime.now().date()))
            
            print(f"[OK] Student record created successfully!")
            
            cursor.connection.commit()
            print(f"[SUCCESS] Student '{first_name} {last_name}' added successfully!")
            print(f"  Admission Number: {admission_number}")
            print(f"  Username: {username}")
            print(f"  Password: {admission_number} (default)")
            return True
            
        except Exception as e:
            print(f"\n[ERROR] Error adding student: {str(e)}")
            import traceback
            traceback.print_exc()
            cursor.connection.rollback()
            return False

if __name__ == '__main__':
    print("=" * 60)
    print("TEST ADD TEACHER AND STUDENT")
    print("=" * 60)
    
    result1 = test_teacher_add()
    result2 = test_student_add()
    
    print("\n" + "=" * 60)
    if result1 and result2:
        print("[SUCCESS] All tests passed!")
    else:
        print("[FAILED] Some tests failed. Check errors above.")
    print("=" * 60)
