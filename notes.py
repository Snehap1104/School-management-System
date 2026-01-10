"""
Notes Management Blueprint
Handles note upload, view, and download with role-based access
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, session, abort
from database import get_db
from utils import require_login, require_role, secure_file_save, delete_file, allowed_file
from config import Config
from datetime import datetime
import os

notes_bp = Blueprint('notes', __name__, url_prefix='/notes')

# ============================================
# NOTES UPLOAD (Teacher only)
# ============================================

@notes_bp.route('/upload', methods=['GET', 'POST'])
@require_login
@require_role('teacher')
def upload_notes():
    """Upload study notes (PDF, DOC, DOCX, PPT) - Teacher only"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        subject_id = request.form.get('subject_id')
        class_id = request.form.get('class_id')
        section_id = request.form.get('section_id') or None
        description = request.form.get('description', '').strip()
        file = request.files.get('file')
        academic_year_id = request.form.get('academic_year_id')
        
        if not title or not subject_id or not class_id or not file:
            flash('Title, subject, class, and file are required.', 'danger')
            return redirect(url_for('notes.upload_notes'))
        
        if file.filename == '':
            flash('Please select a file to upload.', 'danger')
            return redirect(url_for('notes.upload_notes'))
        
        # Check file type
        if not allowed_file(file.filename):
            flash('Invalid file type. Allowed types: PDF, DOC, DOCX, PPT, PPTX', 'danger')
            return redirect(url_for('notes.upload_notes'))
        
        try:
            cursor = get_db()
            
            # Get teacher_id from user_id
            user_id = session.get('user_id')
            cursor.execute("SELECT id FROM teachers WHERE user_id = %s", (user_id,))
            teacher = cursor.fetchone()
            
            if not teacher:
                flash('Teacher profile not found.', 'danger')
                return redirect(url_for('auth.logout'))
            
            teacher_id = teacher[0]
            
            # Get current academic year if not specified
            if not academic_year_id:
                cursor.execute("SELECT id FROM academic_years WHERE is_current = TRUE LIMIT 1")
                academic_year = cursor.fetchone()
                academic_year_id = academic_year[0] if academic_year else None
            
            # Save file securely
            success, file_path, error = secure_file_save(file, Config.NOTES_FOLDER)
            if not success:
                flash(f'Error uploading file: {error}', 'danger')
                return redirect(url_for('notes.upload_notes'))
            
            # Get file metadata
            file_size = os.path.getsize(file_path)
            original_filename = file.filename
            file_type = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
            
            # Save note metadata to database
            cursor.execute("""
                INSERT INTO notes 
                (title, file_name, original_file_name, file_path, file_size, file_type,
                 subject_id, class_id, section_id, teacher_id, academic_year_id, description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (title, os.path.basename(file_path), original_filename, file_path, file_size, file_type,
                  subject_id, class_id, section_id, teacher_id, academic_year_id, description or None))
            
            cursor.connection.commit()
            flash('Notes uploaded successfully!', 'success')
            return redirect(url_for('notes.list_notes'))
        
        except Exception as e:
            cursor.connection.rollback()
            flash(f'Error uploading notes: {str(e)}', 'danger')
            if 'file_path' in locals() and os.path.exists(file_path):
                delete_file(file_path)
            return redirect(url_for('notes.upload_notes'))
    
    # GET request - show upload form
    try:
        cursor = get_db()
        cursor.execute("SELECT id, subject_name FROM subjects ORDER BY subject_name")
        subjects = cursor.fetchall()
        
        cursor.execute("SELECT id, class_name FROM classes ORDER BY class_name")
        classes = cursor.fetchall()
        
        cursor.execute("SELECT id, section_name, class_id FROM sections ORDER BY class_id, section_name")
        sections = cursor.fetchall()
        
        cursor.execute("SELECT id, year_name FROM academic_years ORDER BY start_date DESC")
        academic_years = cursor.fetchall()
        
        return render_template('notes/upload.html',
                             subjects=subjects, classes=classes, sections=sections, academic_years=academic_years)
    except Exception as e:
        flash(f'Error loading form: {str(e)}', 'danger')
        return render_template('notes/upload.html', subjects=[], classes=[], sections=[], academic_years=[])

# ============================================
# NOTES LISTING
# ============================================

@notes_bp.route('/list')
@require_login
def list_notes():
    """List notes based on user role"""
    try:
        cursor = get_db()
        user_role = session.get('role')
        user_id = session.get('user_id')
        
        # Filter options
        subject_id = request.args.get('subject_id', type=int)
        class_id = request.args.get('class_id', type=int)
        section_id = request.args.get('section_id', type=int)
        search = request.args.get('search', '').strip()
        
        if user_role == 'teacher':
            # Teachers can see their own notes
            cursor.execute("SELECT id FROM teachers WHERE user_id = %s", (user_id,))
            teacher = cursor.fetchone()
            if not teacher:
                flash('Teacher profile not found.', 'danger')
                return redirect(url_for('auth.logout'))
            
            teacher_id = teacher[0]
            
            query = """
                SELECT n.id, n.title, n.original_file_name, n.file_size, n.file_type, n.upload_date,
                       s.subject_name, c.class_name, sec.section_name, t.first_name, t.last_name
                FROM notes n
                JOIN subjects s ON n.subject_id = s.id
                JOIN classes c ON n.class_id = c.id
                LEFT JOIN sections sec ON n.section_id = sec.id
                JOIN teachers t ON n.teacher_id = t.id
                WHERE n.teacher_id = %s AND n.is_active = TRUE
            """
            params = [teacher_id]
            
        elif user_role == 'student':
            # Students can see notes for their class
            cursor.execute("""
                SELECT s.class_id, s.section_id FROM students s WHERE s.user_id = %s
            """, (user_id,))
            student = cursor.fetchone()
            
            if not student:
                flash('Student profile not found.', 'danger')
                return redirect(url_for('auth.logout'))
            
            student_class_id = student[0]
            student_section_id = student[1]
            
            query = """
                SELECT n.id, n.title, n.original_file_name, n.file_size, n.file_type, n.upload_date,
                       s.subject_name, c.class_name, sec.section_name, t.first_name, t.last_name
                FROM notes n
                JOIN subjects s ON n.subject_id = s.id
                JOIN classes c ON n.class_id = c.id
                LEFT JOIN sections sec ON n.section_id = sec.id
                JOIN teachers t ON n.teacher_id = t.id
                WHERE n.class_id = %s AND (n.section_id = %s OR n.section_id IS NULL) AND n.is_active = TRUE
            """
            params = [student_class_id, student_section_id]
            
        else:  # admin
            # Admin can see all notes
            query = """
                SELECT n.id, n.title, n.original_file_name, n.file_size, n.file_type, n.upload_date,
                       s.subject_name, c.class_name, sec.section_name, t.first_name, t.last_name
                FROM notes n
                JOIN subjects s ON n.subject_id = s.id
                JOIN classes c ON n.class_id = c.id
                LEFT JOIN sections sec ON n.section_id = sec.id
                JOIN teachers t ON n.teacher_id = t.id
                WHERE n.is_active = TRUE
            """
            params = []
        
        # Apply filters
        if subject_id:
            query += " AND n.subject_id = %s"
            params.append(subject_id)
        
        if class_id:
            query += " AND n.class_id = %s"
            params.append(class_id)
        
        if section_id:
            query += " AND n.section_id = %s"
            params.append(section_id)
        
        if search:
            query += " AND (n.title LIKE %s OR s.subject_name LIKE %s)"
            search_param = f"%{search}%"
            params.extend([search_param, search_param])
        
        query += " ORDER BY n.upload_date DESC"
        
        cursor.execute(query, params)
        notes_list = cursor.fetchall()
        
        # Get filter options
        cursor.execute("SELECT id, subject_name FROM subjects ORDER BY subject_name")
        subjects = cursor.fetchall()
        
        cursor.execute("SELECT id, class_name FROM classes ORDER BY class_name")
        classes = cursor.fetchall()
        
        cursor.execute("SELECT id, section_name, class_id FROM sections ORDER BY class_id, section_name")
        sections = cursor.fetchall()
        
        return render_template('notes/list.html',
                             notes=notes_list,
                             subjects=subjects,
                             classes=classes,
                             sections=sections,
                             selected_subject=subject_id,
                             selected_class=class_id,
                             selected_section=section_id,
                             search_query=search)
    
    except Exception as e:
        flash(f'Error loading notes: {str(e)}', 'danger')
        return render_template('notes/list.html', notes=[], subjects=[], classes=[], sections=[])

# ============================================
# NOTES DOWNLOAD
# ============================================

@notes_bp.route('/download/<int:note_id>')
@require_login
def download_notes(note_id):
    """Download notes file - Role-based access"""
    try:
        cursor = get_db()
        user_role = session.get('role')
        user_id = session.get('user_id')
        
        # Get note details
        cursor.execute("""
            SELECT n.id, n.file_path, n.original_file_name, n.class_id, n.section_id, n.teacher_id
            FROM notes n
            WHERE n.id = %s AND n.is_active = TRUE
        """, (note_id,))
        note = cursor.fetchone()
        
        if not note:
            flash('Note not found.', 'danger')
            return redirect(url_for('notes.list_notes'))
        
        file_path = note[1]
        original_filename = note[2]
        note_class_id = note[3]
        note_section_id = note[4]
        note_teacher_id = note[5]
        
        # Role-based access control
        if user_role == 'student':
            # Students can only download notes for their class
            cursor.execute("SELECT class_id, section_id FROM students WHERE user_id = %s", (user_id,))
            student = cursor.fetchone()
            if not student or student[0] != note_class_id:
                abort(403)  # Forbidden
            if note_section_id and student[1] != note_section_id:
                abort(403)
        
        elif user_role == 'teacher':
            # Teachers can only download their own notes
            cursor.execute("SELECT id FROM teachers WHERE user_id = %s", (user_id,))
            teacher = cursor.fetchone()
            if not teacher or teacher[0] != note_teacher_id:
                abort(403)
        
        # Admin can download any note
        
        if not os.path.exists(file_path):
            flash('File not found on server.', 'danger')
            return redirect(url_for('notes.list_notes'))
        
        return send_file(file_path, as_attachment=True, download_name=original_filename)
    
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'danger')
        return redirect(url_for('notes.list_notes'))

@notes_bp.route('/delete/<int:note_id>', methods=['POST'])
@require_login
@require_role('teacher', 'admin')
def delete_notes(note_id):
    """Delete notes - Teacher can only delete their own"""
    try:
        cursor = get_db()
        user_role = session.get('role')
        user_id = session.get('user_id')
        
        # Get note details
        cursor.execute("SELECT file_path, teacher_id FROM notes WHERE id = %s", (note_id,))
        note = cursor.fetchone()
        
        if not note:
            flash('Note not found.', 'danger')
            return redirect(url_for('notes.list_notes'))
        
        file_path = note[0]
        note_teacher_id = note[1]
        
        # Teachers can only delete their own notes
        if user_role == 'teacher':
            cursor.execute("SELECT id FROM teachers WHERE user_id = %s", (user_id,))
            teacher = cursor.fetchone()
            if not teacher or teacher[0] != note_teacher_id:
                flash('You can only delete your own notes.', 'danger')
                return redirect(url_for('notes.list_notes'))
        
        # Soft delete (set is_active = FALSE) instead of hard delete
        cursor.execute("UPDATE notes SET is_active = FALSE WHERE id = %s", (note_id,))
        cursor.connection.commit()
        
        # Optionally delete physical file
        # delete_file(file_path)
        
        flash('Note deleted successfully!', 'success')
    except Exception as e:
        cursor.connection.rollback()
        flash(f'Error deleting note: {str(e)}', 'danger')
    
    return redirect(url_for('notes.list_notes'))
