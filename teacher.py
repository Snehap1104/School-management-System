"""
Teacher Blueprint
Handles teacher operations: CRUD, subject assignment, class assignment
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import get_db
from utils import require_login, require_role, hash_password
from config import Config
from datetime import datetime

teacher_bp = Blueprint('teacher', __name__, url_prefix='/teacher')

@teacher_bp.route('/dashboard')
@require_login
@require_role('teacher')
def dashboard():
    """Teacher dashboard"""
    try:
        user_id = session.get('user_id')
        cursor = get_db()
        
        # Get teacher info
        cursor.execute("""
            SELECT t.id, t.first_name, t.last_name, t.employee_id, t.phone, t.email
            FROM teachers t
            WHERE t.user_id = %s
        """, (user_id,))
        teacher = cursor.fetchone()
        
        if not teacher:
            flash('Teacher profile not found.', 'danger')
            return redirect(url_for('auth.logout'))
        
        teacher_id = teacher[0]
        
        # Get assigned classes
        cursor.execute("""
            SELECT DISTINCT c.id, c.class_name, sec.section_name
            FROM class_teachers ct
            JOIN classes c ON ct.class_id = c.id
            JOIN sections sec ON ct.section_id = sec.id
            WHERE ct.teacher_id = %s
        """, (teacher_id,))
        assigned_classes = cursor.fetchall()
        
        # Get assigned subjects
        cursor.execute("""
            SELECT DISTINCT s.id, s.subject_name, s.subject_code, c.class_name, sec.section_name
            FROM teacher_subjects ts
            JOIN subjects s ON ts.subject_id = s.id
            LEFT JOIN classes c ON ts.class_id = c.id
            LEFT JOIN sections sec ON ts.section_id = sec.id
            WHERE ts.teacher_id = %s
        """, (teacher_id,))
        assigned_subjects = cursor.fetchall()
        
        # Get total notes uploaded
        cursor.execute("SELECT COUNT(*) FROM notes WHERE teacher_id = %s AND is_active = TRUE", (teacher_id,))
        total_notes = cursor.fetchone()[0]
        
        return render_template('teacher/dashboard.html',
                             teacher=teacher,
                             assigned_classes=assigned_classes,
                             assigned_subjects=assigned_subjects,
                             total_notes=total_notes)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'danger')
        return render_template('teacher/dashboard.html')

# ============================================
# TEACHER MANAGEMENT (Admin access)
# ============================================

@teacher_bp.route('/list')
@require_login
@require_role('admin')
def list_teachers():
    """List all teachers"""
    try:
        cursor = get_db()
        cursor.execute("""
            SELECT t.id, t.employee_id, t.first_name, t.last_name, t.phone, t.email,
                   t.qualification, t.is_active
            FROM teachers t
            ORDER BY t.created_at DESC
        """)
        teachers_list = cursor.fetchall()
        return render_template('teacher/list.html', teachers=teachers_list)
    except Exception as e:
        flash(f'Error loading teachers: {str(e)}', 'danger')
        return render_template('teacher/list.html', teachers=[])

@teacher_bp.route('/add', methods=['GET', 'POST'])
@require_login
@require_role('admin')
def add_teacher():
    """Add new teacher"""
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        employee_id = request.form.get('employee_id', '').strip().upper()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        address = request.form.get('address', '').strip()
        qualification = request.form.get('qualification', '').strip()
        specialization = request.form.get('specialization', '').strip()
        hire_date = request.form.get('hire_date')
        is_active = request.form.get('is_active') == 'on'
        
        # User credentials
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not first_name or not last_name or not employee_id or not username or not password:
            flash('Required fields are missing.', 'danger')
            return redirect(url_for('teacher.add_teacher'))
        
        try:
            cursor = get_db()
            
            # Check if employee_id exists
            cursor.execute("SELECT id FROM teachers WHERE employee_id = %s", (employee_id,))
            if cursor.fetchone():
                flash('Employee ID already exists.', 'danger')
                return redirect(url_for('teacher.add_teacher'))
            
            # Check if username exists
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                flash('Username already exists.', 'danger')
                return redirect(url_for('teacher.add_teacher'))
            
            # Create user account
            password_hash = hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, email, password_hash, role, is_active) VALUES (%s, %s, %s, %s, %s)",
                (username, email or f'{username}@school.com', password_hash, 'teacher', is_active)
            )
            user_id = cursor.lastrowid
            
            # Create teacher record (Note: teachers table doesn't have email column)
            cursor.execute("""
                INSERT INTO teachers 
                (user_id, first_name, last_name, employee_id, phone, address,
                 qualification, specialization, hire_date, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (user_id, first_name, last_name, employee_id, phone or None,
                  address or None, qualification or None, specialization or None,
                  hire_date or None, is_active))
            
            cursor.connection.commit()
            flash('Teacher added successfully!', 'success')
            return redirect(url_for('teacher.list_teachers'))
        
        except Exception as e:
            cursor.connection.rollback()
            flash(f'Error adding teacher: {str(e)}', 'danger')
            return redirect(url_for('teacher.add_teacher'))
    
    # GET request - show form
    return render_template('teacher/add.html')

@teacher_bp.route('/edit/<int:teacher_id>', methods=['GET', 'POST'])
@require_login
@require_role('admin')
def edit_teacher(teacher_id):
    """Edit teacher information"""
    try:
        cursor = get_db()
        
        if request.method == 'POST':
            first_name = request.form.get('first_name', '').strip()
            last_name = request.form.get('last_name', '').strip()
            employee_id = request.form.get('employee_id', '').strip().upper()
            phone = request.form.get('phone', '').strip()
            email = request.form.get('email', '').strip()
            address = request.form.get('address', '').strip()
            qualification = request.form.get('qualification', '').strip()
            specialization = request.form.get('specialization', '').strip()
            hire_date = request.form.get('hire_date')
            is_active = request.form.get('is_active') == 'on'
            
            if not first_name or not last_name or not employee_id:
                flash('Required fields are missing.', 'danger')
                return redirect(url_for('teacher.edit_teacher', teacher_id=teacher_id))
            
            # Check if employee_id exists for other teachers
            cursor.execute("SELECT id FROM teachers WHERE employee_id = %s AND id != %s", (employee_id, teacher_id))
            if cursor.fetchone():
                flash('Employee ID already exists.', 'danger')
                return redirect(url_for('teacher.edit_teacher', teacher_id=teacher_id))
            
            # Update teacher
            cursor.execute("""
                UPDATE teachers SET
                first_name = %s, last_name = %s, employee_id = %s, phone = %s,
                email = %s, address = %s, qualification = %s, specialization = %s,
                hire_date = %s, is_active = %s
                WHERE id = %s
            """, (first_name, last_name, employee_id, phone or None, email or None,
                  address or None, qualification or None, specialization or None,
                  hire_date or None, is_active, teacher_id))
            
            # Update user status
            cursor.execute("SELECT user_id FROM teachers WHERE id = %s", (teacher_id,))
            teacher = cursor.fetchone()
            if teacher:
                cursor.execute("UPDATE users SET is_active = %s WHERE id = %s", (is_active, teacher[0]))
            
            cursor.connection.commit()
            flash('Teacher updated successfully!', 'success')
            return redirect(url_for('teacher.list_teachers'))
        
        # GET request - load teacher
        cursor.execute("""
            SELECT t.*, u.username, u.email as user_email
            FROM teachers t
            JOIN users u ON t.user_id = u.id
            WHERE t.id = %s
        """, (teacher_id,))
        teacher = cursor.fetchone()
        
        if not teacher:
            flash('Teacher not found.', 'danger')
            return redirect(url_for('teacher.list_teachers'))
        
        return render_template('teacher/edit.html', teacher=teacher)
    
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('teacher.list_teachers'))

@teacher_bp.route('/delete/<int:teacher_id>', methods=['POST'])
@require_login
@require_role('admin')
def delete_teacher(teacher_id):
    """Delete teacher"""
    try:
        cursor = get_db()
        # Delete teacher (cascades to user via foreign key)
        cursor.execute("DELETE FROM teachers WHERE id = %s", (teacher_id,))
        cursor.connection.commit()
        flash('Teacher deleted successfully!', 'success')
    except Exception as e:
        cursor.connection.rollback()
        flash(f'Error deleting teacher: {str(e)}', 'danger')
    return redirect(url_for('teacher.list_teachers'))

# ============================================
# CLASS & SUBJECT ASSIGNMENT (Admin)
# ============================================

@teacher_bp.route('/assign-class', methods=['GET', 'POST'])
@require_login
@require_role('admin')
def assign_class():
    """Assign teacher to class and section"""
    if request.method == 'POST':
        teacher_id = request.form.get('teacher_id')
        class_id = request.form.get('class_id')
        section_id = request.form.get('section_id')
        academic_year_id = request.form.get('academic_year_id')
        
        if not teacher_id or not class_id or not section_id:
            flash('Teacher, class, and section are required.', 'danger')
            return redirect(url_for('teacher.assign_class'))
        
        try:
            cursor = get_db()
            
            # Get current academic year if not specified
            if not academic_year_id:
                cursor.execute("SELECT id FROM academic_years WHERE is_current = TRUE LIMIT 1")
                academic_year = cursor.fetchone()
                academic_year_id = academic_year[0] if academic_year else None
            
            cursor.execute("""
                INSERT INTO class_teachers (teacher_id, class_id, section_id, academic_year_id, assigned_date)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE assigned_date = %s
            """, (teacher_id, class_id, section_id, academic_year_id, datetime.now().date(),
                  datetime.now().date()))
            cursor.connection.commit()
            flash('Teacher assigned to class successfully!', 'success')
        except Exception as e:
            cursor.connection.rollback()
            flash(f'Error assigning teacher: {str(e)}', 'danger')
        return redirect(url_for('teacher.assign_class'))
    
    # GET request
    try:
        cursor = get_db()
        cursor.execute("SELECT id, employee_id, first_name, last_name FROM teachers WHERE is_active = TRUE")
        teachers = cursor.fetchall()
        
        cursor.execute("SELECT id, class_name FROM classes ORDER BY class_name")
        classes = cursor.fetchall()
        
        cursor.execute("SELECT id, section_name, class_id FROM sections ORDER BY class_id, section_name")
        sections = cursor.fetchall()
        
        cursor.execute("SELECT id, year_name FROM academic_years ORDER BY start_date DESC")
        academic_years = cursor.fetchall()
        
        return render_template('teacher/assign_class.html',
                             teachers=teachers, classes=classes, sections=sections, academic_years=academic_years)
    except Exception as e:
        flash(f'Error loading form: {str(e)}', 'danger')
        return render_template('teacher/assign_class.html', teachers=[], classes=[], sections=[], academic_years=[])

@teacher_bp.route('/assign-subject', methods=['GET', 'POST'])
@require_login
@require_role('admin')
def assign_subject():
    """Assign subject to teacher"""
    if request.method == 'POST':
        teacher_id = request.form.get('teacher_id')
        subject_id = request.form.get('subject_id')
        class_id = request.form.get('class_id') or None
        section_id = request.form.get('section_id') or None
        academic_year_id = request.form.get('academic_year_id')
        
        if not teacher_id or not subject_id:
            flash('Teacher and subject are required.', 'danger')
            return redirect(url_for('teacher.assign_subject'))
        
        try:
            cursor = get_db()
            
            # Get current academic year if not specified
            if not academic_year_id:
                cursor.execute("SELECT id FROM academic_years WHERE is_current = TRUE LIMIT 1")
                academic_year = cursor.fetchone()
                academic_year_id = academic_year[0] if academic_year else None
            
            cursor.execute("""
                INSERT INTO teacher_subjects (teacher_id, subject_id, class_id, section_id, academic_year_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (teacher_id, subject_id, class_id, section_id, academic_year_id))
            cursor.connection.commit()
            flash('Subject assigned to teacher successfully!', 'success')
        except Exception as e:
            cursor.connection.rollback()
            flash(f'Error assigning subject: {str(e)}', 'danger')
        return redirect(url_for('teacher.assign_subject'))
    
    # GET request
    try:
        cursor = get_db()
        cursor.execute("SELECT id, employee_id, first_name, last_name FROM teachers WHERE is_active = TRUE")
        teachers = cursor.fetchall()
        
        cursor.execute("SELECT id, subject_name, subject_code FROM subjects ORDER BY subject_name")
        subjects = cursor.fetchall()
        
        cursor.execute("SELECT id, class_name FROM classes ORDER BY class_name")
        classes = cursor.fetchall()
        
        cursor.execute("SELECT id, section_name, class_id FROM sections ORDER BY class_id, section_name")
        sections = cursor.fetchall()
        
        cursor.execute("SELECT id, year_name FROM academic_years ORDER BY start_date DESC")
        academic_years = cursor.fetchall()
        
        return render_template('teacher/assign_subject.html',
                             teachers=teachers, subjects=subjects, classes=classes, sections=sections, academic_years=academic_years)
    except Exception as e:
        flash(f'Error loading form: {str(e)}', 'danger')
        return render_template('teacher/assign_subject.html', teachers=[], subjects=[], classes=[], sections=[], academic_years=[])
