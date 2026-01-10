"""
Admin Blueprint
Handles admin operations: user management, classes, sections, subjects, dashboard
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from database import get_db
from utils import require_login, require_role, hash_password
from config import Config
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@require_login
@require_role('admin')
def dashboard():
    """Admin dashboard with statistics"""
    try:
        cursor = get_db()
        
        # Get statistics
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'student' AND is_active = TRUE")
        total_students = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'teacher' AND is_active = TRUE")
        total_teachers = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM classes")
        total_classes = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM subjects")
        total_subjects = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM notes WHERE is_active = TRUE")
        total_notes = cursor.fetchone()[0]
        
        # Recent activities
        cursor.execute("""
            SELECT u.username, u.role, u.created_at 
            FROM users u 
            ORDER BY u.created_at DESC 
            LIMIT 5
        """)
        recent_users = cursor.fetchall()
        
        return render_template('admin/dashboard.html',
                             total_students=total_students,
                             total_teachers=total_teachers,
                             total_classes=total_classes,
                             total_subjects=total_subjects,
                             total_notes=total_notes,
                             recent_users=recent_users)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'danger')
        return render_template('admin/dashboard.html')

# ============================================
# USER MANAGEMENT
# ============================================

@admin_bp.route('/users')
@require_login
@require_role('admin')
def users():
    """List all users"""
    try:
        cursor = get_db()
        cursor.execute("""
            SELECT u.id, u.username, u.email, u.role, u.is_active, u.created_at
            FROM users u
            ORDER BY u.created_at DESC
        """)
        users_list = cursor.fetchall()
        return render_template('admin/users.html', users=users_list)
    except Exception as e:
        flash(f'Error loading users: {str(e)}', 'danger')
        return render_template('admin/users.html', users=[])

@admin_bp.route('/users/add', methods=['GET', 'POST'])
@require_login
@require_role('admin')
def add_user():
    """Add new user"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'student')
        is_active = request.form.get('is_active') == 'on'
        
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('admin/user_form.html', user=None)
        
        try:
            cursor = get_db()
            # Check if username or email exists
            cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
            if cursor.fetchone():
                flash('Username or email already exists.', 'danger')
                return render_template('admin/user_form.html', user=None)
            
            # Create user
            password_hash = hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, email, password_hash, role, is_active) VALUES (%s, %s, %s, %s, %s)",
                (username, email, password_hash, role, is_active)
            )
            cursor.connection.commit()
            flash('User created successfully!', 'success')
            return redirect(url_for('admin.users'))
        
        except Exception as e:
            cursor.connection.rollback()
            flash(f'Error creating user: {str(e)}', 'danger')
            return render_template('admin/user_form.html', user=None)
    
    return render_template('admin/user_form.html', user=None)

@admin_bp.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@require_login
@require_role('admin')
def edit_user(user_id):
    """Edit existing user"""
    try:
        cursor = get_db()
        
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            role = request.form.get('role', 'student')
            is_active = request.form.get('is_active') == 'on'
            
            if not username or not email:
                flash('Username and email are required.', 'danger')
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                user = cursor.fetchone()
                return render_template('admin/user_form.html', user=user)
            
            # Check if username or email exists for other users
            cursor.execute("SELECT id FROM users WHERE (username = %s OR email = %s) AND id != %s", 
                         (username, email, user_id))
            if cursor.fetchone():
                flash('Username or email already exists.', 'danger')
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                user = cursor.fetchone()
                return render_template('admin/user_form.html', user=user)
            
            # Update user
            if password:
                password_hash = hash_password(password)
                cursor.execute(
                    "UPDATE users SET username = %s, email = %s, password_hash = %s, role = %s, is_active = %s WHERE id = %s",
                    (username, email, password_hash, role, is_active, user_id)
                )
            else:
                cursor.execute(
                    "UPDATE users SET username = %s, email = %s, role = %s, is_active = %s WHERE id = %s",
                    (username, email, role, is_active, user_id)
                )
            cursor.connection.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('admin.users'))
        
        # GET request - load user
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            flash('User not found.', 'danger')
            return redirect(url_for('admin.users'))
        
        return render_template('admin/user_form.html', user=user)
    
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('admin.users'))

@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@require_login
@require_role('admin')
def delete_user(user_id):
    """Delete user"""
    try:
        cursor = get_db()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        cursor.connection.commit()
        flash('User deleted successfully!', 'success')
    except Exception as e:
        cursor.connection.rollback()
        flash(f'Error deleting user: {str(e)}', 'danger')
    return redirect(url_for('admin.users'))

# ============================================
# CLASS MANAGEMENT
# ============================================

@admin_bp.route('/classes')
@require_login
@require_role('admin')
def classes():
    """List all classes"""
    try:
        cursor = get_db()
        cursor.execute("""
            SELECT c.id, c.class_name, c.class_code, c.description, ay.year_name
            FROM classes c
            LEFT JOIN academic_years ay ON c.academic_year_id = ay.id
            ORDER BY c.class_name
        """)
        classes_list = cursor.fetchall()
        
        cursor.execute("SELECT id, year_name, is_current FROM academic_years ORDER BY start_date DESC")
        academic_years = cursor.fetchall()
        
        return render_template('admin/classes.html', classes=classes_list, academic_years=academic_years)
    except Exception as e:
        flash(f'Error loading classes: {str(e)}', 'danger')
        return render_template('admin/classes.html', classes=[], academic_years=[])

@admin_bp.route('/classes/add', methods=['POST'])
@require_login
@require_role('admin')
def add_class():
    """Add new class"""
    class_name = request.form.get('class_name', '').strip()
    class_code = request.form.get('class_code', '').strip()
    description = request.form.get('description', '').strip()
    academic_year_id = request.form.get('academic_year_id')
    
    if not class_name:
        flash('Class name is required.', 'danger')
        return redirect(url_for('admin.classes'))
    
    try:
        cursor = get_db()
        cursor.execute(
            "INSERT INTO classes (class_name, class_code, description, academic_year_id) VALUES (%s, %s, %s, %s)",
            (class_name, class_code or None, description or None, academic_year_id or None)
        )
        cursor.connection.commit()
        flash('Class added successfully!', 'success')
    except Exception as e:
        cursor.connection.rollback()
        flash(f'Error adding class: {str(e)}', 'danger')
    
    return redirect(url_for('admin.classes'))

@admin_bp.route('/classes/delete/<int:class_id>', methods=['POST'])
@require_login
@require_role('admin')
def delete_class(class_id):
    """Delete class"""
    try:
        cursor = get_db()
        cursor.execute("DELETE FROM classes WHERE id = %s", (class_id,))
        cursor.connection.commit()
        flash('Class deleted successfully!', 'success')
    except Exception as e:
        cursor.connection.rollback()
        flash(f'Error deleting class: {str(e)}', 'danger')
    return redirect(url_for('admin.classes'))

# ============================================
# SECTION MANAGEMENT
# ============================================

@admin_bp.route('/sections')
@require_login
@require_role('admin')
def sections():
    """List all sections"""
    try:
        cursor = get_db()
        cursor.execute("""
            SELECT s.id, s.section_name, c.class_name, s.capacity, ay.year_name
            FROM sections s
            LEFT JOIN classes c ON s.class_id = c.id
            LEFT JOIN academic_years ay ON s.academic_year_id = ay.id
            ORDER BY c.class_name, s.section_name
        """)
        sections_list = cursor.fetchall()
        
        cursor.execute("SELECT id, class_name FROM classes ORDER BY class_name")
        classes_list = cursor.fetchall()
        
        cursor.execute("SELECT id, year_name FROM academic_years ORDER BY start_date DESC")
        academic_years = cursor.fetchall()
        
        return render_template('admin/sections.html', 
                             sections=sections_list, 
                             classes=classes_list,
                             academic_years=academic_years)
    except Exception as e:
        flash(f'Error loading sections: {str(e)}', 'danger')
        return render_template('admin/sections.html', sections=[], classes=[], academic_years=[])

@admin_bp.route('/sections/add', methods=['POST'])
@require_login
@require_role('admin')
def add_section():
    """Add new section"""
    section_name = request.form.get('section_name', '').strip().upper()
    class_id = request.form.get('class_id')
    capacity = request.form.get('capacity', 40)
    academic_year_id = request.form.get('academic_year_id')
    
    if not section_name or not class_id:
        flash('Section name and class are required.', 'danger')
        return redirect(url_for('admin.sections'))
    
    try:
        cursor = get_db()
        cursor.execute(
            "INSERT INTO sections (section_name, class_id, capacity, academic_year_id) VALUES (%s, %s, %s, %s)",
            (section_name, class_id, capacity, academic_year_id or None)
        )
        cursor.connection.commit()
        flash('Section added successfully!', 'success')
    except Exception as e:
        cursor.connection.rollback()
        flash(f'Error adding section: {str(e)}', 'danger')
    
    return redirect(url_for('admin.sections'))

@admin_bp.route('/sections/delete/<int:section_id>', methods=['POST'])
@require_login
@require_role('admin')
def delete_section(section_id):
    """Delete section"""
    try:
        cursor = get_db()
        cursor.execute("DELETE FROM sections WHERE id = %s", (section_id,))
        cursor.connection.commit()
        flash('Section deleted successfully!', 'success')
    except Exception as e:
        cursor.connection.rollback()
        flash(f'Error deleting section: {str(e)}', 'danger')
    return redirect(url_for('admin.sections'))

# ============================================
# SUBJECT MANAGEMENT
# ============================================

@admin_bp.route('/subjects')
@require_login
@require_role('admin')
def subjects():
    """List all subjects"""
    try:
        cursor = get_db()
        cursor.execute("SELECT id, subject_name, subject_code, description FROM subjects ORDER BY subject_name")
        subjects_list = cursor.fetchall()
        return render_template('admin/subjects.html', subjects=subjects_list)
    except Exception as e:
        flash(f'Error loading subjects: {str(e)}', 'danger')
        return render_template('admin/subjects.html', subjects=[])

@admin_bp.route('/subjects/add', methods=['POST'])
@require_login
@require_role('admin')
def add_subject():
    """Add new subject"""
    subject_name = request.form.get('subject_name', '').strip()
    subject_code = request.form.get('subject_code', '').strip().upper()
    description = request.form.get('description', '').strip()
    
    if not subject_name:
        flash('Subject name is required.', 'danger')
        return redirect(url_for('admin.subjects'))
    
    try:
        cursor = get_db()
        cursor.execute(
            "INSERT INTO subjects (subject_name, subject_code, description) VALUES (%s, %s, %s)",
            (subject_name, subject_code or None, description or None)
        )
        cursor.connection.commit()
        flash('Subject added successfully!', 'success')
    except Exception as e:
        cursor.connection.rollback()
        flash(f'Error adding subject: {str(e)}', 'danger')
    
    return redirect(url_for('admin.subjects'))

@admin_bp.route('/subjects/delete/<int:subject_id>', methods=['POST'])
@require_login
@require_role('admin')
def delete_subject(subject_id):
    """Delete subject"""
    try:
        cursor = get_db()
        cursor.execute("DELETE FROM subjects WHERE id = %s", (subject_id,))
        cursor.connection.commit()
        flash('Subject deleted successfully!', 'success')
    except Exception as e:
        cursor.connection.rollback()
        flash(f'Error deleting subject: {str(e)}', 'danger')
    return redirect(url_for('admin.subjects'))
