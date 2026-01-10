"""
Student Blueprint
Handles student operations: CRUD, admission, photo upload, search
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, session
from database import get_db
from utils import require_login, require_role, secure_file_save, delete_file, hash_password
from config import Config
from datetime import datetime
import os

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/dashboard')
@require_login
@require_role('student')
def dashboard():
    """Student dashboard"""
    try:
        user_id = session.get('user_id')
        cursor = get_db()
        
        # Get student info
        cursor.execute("""
            SELECT s.id, s.admission_number, s.first_name, s.last_name, s.class_id, s.section_id,
                   c.class_name, sec.section_name
            FROM students s
            LEFT JOIN classes c ON s.class_id = c.id
            LEFT JOIN sections sec ON s.section_id = sec.id
            WHERE s.user_id = %s
        """, (user_id,))
        student = cursor.fetchone()
        
        if not student:
            flash('Student profile not found.', 'danger')
            return redirect(url_for('auth.logout'))
        
        # Get attendance statistics
        cursor.execute("""
            SELECT 
                COUNT(*) as total_days,
                SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present_days,
                SUM(CASE WHEN status = 'absent' THEN 1 ELSE 0 END) as absent_days
            FROM attendance
            WHERE student_id = %s
        """, (student[0],))
        attendance_stats = cursor.fetchone()
        
        # Calculate percentage
        total = attendance_stats[0] if attendance_stats and attendance_stats[0] else 0
        present = attendance_stats[1] if attendance_stats and attendance_stats[1] else 0
        attendance_percentage = (present / total * 100) if total > 0 else 0
        
        # Recent notes for student's class
        cursor.execute("""
            SELECT n.id, n.title, n.upload_date, s.subject_name, t.first_name, t.last_name
            FROM notes n
            LEFT JOIN subjects s ON n.subject_id = s.id
            LEFT JOIN teachers t ON n.teacher_id = t.id
            WHERE n.class_id = %s AND n.is_active = TRUE
            ORDER BY n.upload_date DESC
            LIMIT 5
        """, (student[4],))
        recent_notes = cursor.fetchall()
        
        return render_template('student/dashboard.html',
                             student=student,
                             attendance_percentage=round(attendance_percentage, 2),
                             attendance_stats=attendance_stats,
                             recent_notes=recent_notes)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'danger')
        return render_template('student/dashboard.html')

# ============================================
# STUDENT MANAGEMENT (Admin & Teacher access)
# ============================================

@student_bp.route('/list')
@require_login
def list_students():
    """List all students with search and filter"""
    try:
        cursor = get_db()
        class_id = request.args.get('class_id', type=int)
        search = request.args.get('search', '').strip()
        
        query = """
            SELECT s.id, s.admission_number, s.first_name, s.last_name, s.phone, s.email,
                   c.class_name, sec.section_name, s.is_active
            FROM students s
            LEFT JOIN classes c ON s.class_id = c.id
            LEFT JOIN sections sec ON s.section_id = sec.id
            WHERE 1=1
        """
        params = []
        
        if class_id:
            query += " AND s.class_id = %s"
            params.append(class_id)
        
        if search:
            query += " AND (s.first_name LIKE %s OR s.last_name LIKE %s OR s.admission_number LIKE %s)"
            search_param = f"%{search}%"
            params.extend([search_param, search_param, search_param])
        
        query += " ORDER BY s.created_at DESC"
        
        cursor.execute(query, params)
        students_list = cursor.fetchall()
        
        # Get classes for filter
        cursor.execute("SELECT id, class_name FROM classes ORDER BY class_name")
        classes_list = cursor.fetchall()
        
        return render_template('student/list.html',
                             students=students_list,
                             classes=classes_list,
                             selected_class=class_id,
                             search_query=search)
    except Exception as e:
        flash(f'Error loading students: {str(e)}', 'danger')
        return render_template('student/list.html', students=[], classes=[])

@student_bp.route('/add', methods=['GET', 'POST'])
@require_login
@require_role('admin', 'teacher')
def add_student():
    """Add new student with auto-generated admission number"""
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        date_of_birth = request.form.get('date_of_birth')
        gender = request.form.get('gender')
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        address = request.form.get('address', '').strip()
        parent_name = request.form.get('parent_name', '').strip()
        parent_phone = request.form.get('parent_phone', '').strip()
        parent_email = request.form.get('parent_email', '').strip()
        class_id = request.form.get('class_id')
        section_id = request.form.get('section_id')
        admission_date = request.form.get('admission_date') or datetime.now().strftime('%Y-%m-%d')
        
        photo = request.files.get('photo')
        
        if not first_name or not last_name:
            flash('First name and last name are required.', 'danger')
            return redirect(url_for('student.add_student'))
        
        try:
            cursor = get_db()
            
            # Generate unique admission number
            year = datetime.now().year
            cursor.execute("SELECT COUNT(*) FROM students WHERE admission_number LIKE %s", (f'ADM{year}%',))
            count = cursor.fetchone()[0]
            admission_number = f'ADM{year}{str(count + 1).zfill(4)}'
            
            # Create user account for student
            username = admission_number.lower()
            password = hash_password(admission_number)  # Default password is admission number
            
            cursor.execute(
                "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
                (username, email or f'{username}@school.com', password, 'student')
            )
            user_id = cursor.lastrowid
            
            # Handle photo upload
            photo_path = None
            if photo and photo.filename:
                success, file_path, error = secure_file_save(photo, Config.STUDENT_PHOTOS_FOLDER)
                if success:
                    photo_path = file_path
                else:
                    flash(f'Photo upload failed: {error}', 'warning')
            
            # Get current academic year
            cursor.execute("SELECT id FROM academic_years WHERE is_current = TRUE LIMIT 1")
            academic_year = cursor.fetchone()
            academic_year_id = academic_year[0] if academic_year else None
            
            # Create student record
            cursor.execute("""
                INSERT INTO students 
                (user_id, admission_number, first_name, last_name, date_of_birth, gender, 
                 phone, email, address, parent_name, parent_phone, parent_email, 
                 class_id, section_id, academic_year_id, photo_path, admission_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (user_id, admission_number, first_name, last_name, date_of_birth or None, gender,
                  phone or None, email or None, address or None, parent_name or None,
                  parent_phone or None, parent_email or None, class_id or None, section_id or None,
                  academic_year_id, photo_path, admission_date))
            
            cursor.connection.commit()
            flash(f'Student added successfully! Admission Number: {admission_number}', 'success')
            return redirect(url_for('student.list_students'))
        
        except Exception as e:
            cursor.connection.rollback()
            flash(f'Error adding student: {str(e)}', 'danger')
            return redirect(url_for('student.add_student'))
    
    # GET request - show form
    try:
        cursor = get_db()
        cursor.execute("SELECT id, class_name FROM classes ORDER BY class_name")
        classes_list = cursor.fetchall()
        
        cursor.execute("SELECT id, section_name, class_id FROM sections ORDER BY class_id, section_name")
        sections_list = cursor.fetchall()
        
        return render_template('student/add.html', classes=classes_list, sections=sections_list)
    except Exception as e:
        flash(f'Error loading form: {str(e)}', 'danger')
        return render_template('student/add.html', classes=[], sections=[])

@student_bp.route('/edit/<int:student_id>', methods=['GET', 'POST'])
@require_login
@require_role('admin', 'teacher')
def edit_student(student_id):
    """Edit student information"""
    try:
        cursor = get_db()
        
        if request.method == 'POST':
            first_name = request.form.get('first_name', '').strip()
            last_name = request.form.get('last_name', '').strip()
            date_of_birth = request.form.get('date_of_birth')
            gender = request.form.get('gender')
            phone = request.form.get('phone', '').strip()
            email = request.form.get('email', '').strip()
            address = request.form.get('address', '').strip()
            parent_name = request.form.get('parent_name', '').strip()
            parent_phone = request.form.get('parent_phone', '').strip()
            parent_email = request.form.get('parent_email', '').strip()
            class_id = request.form.get('class_id')
            section_id = request.form.get('section_id')
            is_active = request.form.get('is_active') == 'on'
            
            photo = request.files.get('photo')
            
            if not first_name or not last_name:
                flash('First name and last name are required.', 'danger')
                return redirect(url_for('student.edit_student', student_id=student_id))
            
            # Handle photo upload if new photo is provided
            photo_path = None
            old_photo_path = None
            
            # Get old photo path
            cursor.execute("SELECT photo_path FROM students WHERE id = %s", (student_id,))
            old_photo = cursor.fetchone()
            if old_photo and old_photo[0]:
                old_photo_path = old_photo[0]
            
            if photo and photo.filename:
                success, file_path, error = secure_file_save(photo, Config.STUDENT_PHOTOS_FOLDER)
                if success:
                    photo_path = file_path
                    # Delete old photo
                    if old_photo_path:
                        delete_file(old_photo_path)
                else:
                    flash(f'Photo upload failed: {error}', 'warning')
            
            # Update student
            if photo_path:
                cursor.execute("""
                    UPDATE students SET
                    first_name = %s, last_name = %s, date_of_birth = %s, gender = %s,
                    phone = %s, email = %s, address = %s, parent_name = %s,
                    parent_phone = %s, parent_email = %s, class_id = %s, section_id = %s,
                    is_active = %s, photo_path = %s
                    WHERE id = %s
                """, (first_name, last_name, date_of_birth or None, gender,
                      phone or None, email or None, address or None, parent_name or None,
                      parent_phone or None, parent_email or None, class_id or None, section_id or None,
                      is_active, photo_path, student_id))
            else:
                cursor.execute("""
                    UPDATE students SET
                    first_name = %s, last_name = %s, date_of_birth = %s, gender = %s,
                    phone = %s, email = %s, address = %s, parent_name = %s,
                    parent_phone = %s, parent_email = %s, class_id = %s, section_id = %s,
                    is_active = %s
                    WHERE id = %s
                """, (first_name, last_name, date_of_birth or None, gender,
                      phone or None, email or None, address or None, parent_name or None,
                      parent_phone or None, parent_email or None, class_id or None, section_id or None,
                      is_active, student_id))
            
            cursor.connection.commit()
            flash('Student updated successfully!', 'success')
            return redirect(url_for('student.list_students'))
        
        # GET request - load student
        cursor.execute("""
            SELECT * FROM students WHERE id = %s
        """, (student_id,))
        student = cursor.fetchone()
        
        if not student:
            flash('Student not found.', 'danger')
            return redirect(url_for('student.list_students'))
        
        cursor.execute("SELECT id, class_name FROM classes ORDER BY class_name")
        classes_list = cursor.fetchall()
        
        cursor.execute("SELECT id, section_name, class_id FROM sections ORDER BY class_id, section_name")
        sections_list = cursor.fetchall()
        
        return render_template('student/edit.html', student=student, classes=classes_list, sections=sections_list)
    
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('student.list_students'))

@student_bp.route('/delete/<int:student_id>', methods=['POST'])
@require_login
@require_role('admin')
def delete_student(student_id):
    """Delete student"""
    try:
        cursor = get_db()
        # Get user_id before deletion
        cursor.execute("SELECT user_id, photo_path FROM students WHERE id = %s", (student_id,))
        student = cursor.fetchone()
        
        if student:
            # Delete photo if exists
            if student[1]:
                delete_file(student[1])
            
            # Delete student (cascades to user via foreign key)
            cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
            cursor.connection.commit()
            flash('Student deleted successfully!', 'success')
        else:
            flash('Student not found.', 'danger')
    except Exception as e:
        cursor.connection.rollback()
        flash(f'Error deleting student: {str(e)}', 'danger')
    return redirect(url_for('student.list_students'))
