"""
Attendance Management Blueprint
Handles attendance marking, reports, and history
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from database import get_db
from utils import require_login, require_role
from datetime import datetime, date
from collections import defaultdict

attendance_bp = Blueprint('attendance', __name__, url_prefix='/attendance')

# ============================================
# MARK ATTENDANCE (Teacher & Admin)
# ============================================

@attendance_bp.route('/mark', methods=['GET', 'POST'])
@require_login
@require_role('teacher', 'admin')
def mark_attendance():
    """Mark attendance by class and section"""
    if request.method == 'POST':
        class_id = request.form.get('class_id')
        section_id = request.form.get('section_id')
        attendance_date = request.form.get('attendance_date') or datetime.now().strftime('%Y-%m-%d')
        subject_id = request.form.get('subject_id') or None
        
        # Get attendance data from form (student_id: status)
        attendance_data = {}
        for key, value in request.form.items():
            if key.startswith('student_'):
                student_id = key.replace('student_', '')
                attendance_data[student_id] = value
        
        if not class_id or not section_id or not attendance_data:
            flash('Class, section, and attendance data are required.', 'danger')
            return redirect(url_for('attendance.mark_attendance'))
        
        try:
            cursor = get_db()
            user_id = session.get('user_id')
            marked_by = None
            
            # Get teacher_id if user is teacher
            if session.get('role') == 'teacher':
                cursor.execute("SELECT id FROM teachers WHERE user_id = %s", (user_id,))
                teacher = cursor.fetchone()
                marked_by = teacher[0] if teacher else None
            
            # Get current academic year
            cursor.execute("SELECT id FROM academic_years WHERE is_current = TRUE LIMIT 1")
            academic_year = cursor.fetchone()
            academic_year_id = academic_year[0] if academic_year else None
            
            # Check if attendance already marked for this date
            cursor.execute("""
                SELECT COUNT(*) FROM attendance 
                WHERE class_id = %s AND section_id = %s AND attendance_date = %s 
                AND (subject_id = %s OR (subject_id IS NULL AND %s IS NULL))
            """, (class_id, section_id, attendance_date, subject_id, subject_id))
            
            existing_count = cursor.fetchone()[0]
            if existing_count > 0:
                flash('Attendance already marked for this date. Please edit existing attendance.', 'warning')
                return redirect(url_for('attendance.view_attendance', 
                                      class_id=class_id, section_id=section_id, date=attendance_date))
            
            # Insert attendance records
            inserted_count = 0
            for student_id, status in attendance_data.items():
                if status in ['present', 'absent', 'late', 'half_day']:
                    try:
                        cursor.execute("""
                            INSERT INTO attendance 
                            (student_id, class_id, section_id, subject_id, attendance_date, status, marked_by, academic_year_id)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (student_id, class_id, section_id, subject_id, attendance_date, status, marked_by, academic_year_id))
                        inserted_count += 1
                    except Exception as e:
                        # Skip duplicate entries
                        continue
            
            cursor.connection.commit()
            flash(f'Attendance marked successfully for {inserted_count} students!', 'success')
            return redirect(url_for('attendance.view_attendance', 
                                  class_id=class_id, section_id=section_id, date=attendance_date))
        
        except Exception as e:
            cursor.connection.rollback()
            flash(f'Error marking attendance: {str(e)}', 'danger')
            return redirect(url_for('attendance.mark_attendance'))
    
    # GET request - show form
    try:
        cursor = get_db()
        class_id = request.args.get('class_id', type=int)
        section_id = request.args.get('section_id', type=int)
        attendance_date = request.args.get('date') or datetime.now().strftime('%Y-%m-%d')
        
        students = []
        if class_id and section_id:
            cursor.execute("""
                SELECT s.id, s.admission_number, s.first_name, s.last_name, s.photo_path
                FROM students s
                WHERE s.class_id = %s AND s.section_id = %s AND s.is_active = TRUE
                ORDER BY s.first_name, s.last_name
            """, (class_id, section_id))
            students = cursor.fetchall()
        
        # Get filter options
        cursor.execute("SELECT id, class_name FROM classes ORDER BY class_name")
        classes = cursor.fetchall()
        
        cursor.execute("SELECT id, section_name, class_id FROM sections ORDER BY class_id, section_name")
        sections = cursor.fetchall()
        
        cursor.execute("SELECT id, subject_name FROM subjects ORDER BY subject_name")
        subjects = cursor.fetchall()
        
        return render_template('attendance/mark.html',
                             students=students,
                             classes=classes,
                             sections=sections,
                             subjects=subjects,
                             selected_class=class_id,
                             selected_section=section_id,
                             attendance_date=attendance_date)
    except Exception as e:
        flash(f'Error loading form: {str(e)}', 'danger')
        return render_template('attendance/mark.html', students=[], classes=[], sections=[], subjects=[])

# ============================================
# VIEW ATTENDANCE
# ============================================

@attendance_bp.route('/view')
@require_login
def view_attendance():
    """View attendance for a specific date, class, and section"""
    try:
        cursor = get_db()
        class_id = request.args.get('class_id', type=int)
        section_id = request.args.get('section_id', type=int)
        attendance_date = request.args.get('date') or datetime.now().strftime('%Y-%m-%d')
        subject_id = request.args.get('subject_id', type=int)
        
        attendance_records = []
        students = []
        
        if class_id and section_id:
            # Get students
            cursor.execute("""
                SELECT s.id, s.admission_number, s.first_name, s.last_name
                FROM students s
                WHERE s.class_id = %s AND s.section_id = %s AND s.is_active = TRUE
                ORDER BY s.first_name, s.last_name
            """, (class_id, section_id))
            students = cursor.fetchall()
            
            # Get attendance records for the date
            if subject_id:
                cursor.execute("""
                    SELECT student_id, status, remarks
                    FROM attendance
                    WHERE class_id = %s AND section_id = %s AND attendance_date = %s AND subject_id = %s
                """, (class_id, section_id, attendance_date, subject_id))
            else:
                cursor.execute("""
                    SELECT student_id, status, remarks
                    FROM attendance
                    WHERE class_id = %s AND section_id = %s AND attendance_date = %s AND subject_id IS NULL
                """, (class_id, section_id, attendance_date))
            
            attendance_records = {row[0]: {'status': row[1], 'remarks': row[2]} for row in cursor.fetchall()}
        
        # Get filter options
        cursor.execute("SELECT id, class_name FROM classes ORDER BY class_name")
        classes = cursor.fetchall()
        
        cursor.execute("SELECT id, section_name, class_id FROM sections ORDER BY class_id, section_name")
        sections = cursor.fetchall()
        
        cursor.execute("SELECT id, subject_name FROM subjects ORDER BY subject_name")
        subjects = cursor.fetchall()
        
        return render_template('attendance/view.html',
                             students=students,
                             attendance_records=attendance_records,
                             classes=classes,
                             sections=sections,
                             subjects=subjects,
                             selected_class=class_id,
                             selected_section=section_id,
                             selected_subject=subject_id,
                             attendance_date=attendance_date)
    except Exception as e:
        flash(f'Error loading attendance: {str(e)}', 'danger')
        return render_template('attendance/view.html', students=[], attendance_records={}, classes=[], sections=[], subjects=[])

# ============================================
# ATTENDANCE REPORTS
# ============================================

@attendance_bp.route('/reports')
@require_login
@require_role('admin', 'teacher')
def reports():
    """Attendance reports dashboard"""
    try:
        cursor = get_db()
        
        # Get filter options
        cursor.execute("SELECT id, class_name FROM classes ORDER BY class_name")
        classes = cursor.fetchall()
        
        cursor.execute("SELECT id, section_name, class_id FROM sections ORDER BY class_id, section_name")
        sections = cursor.fetchall()
        
        return render_template('attendance/reports.html', classes=classes, sections=sections)
    except Exception as e:
        flash(f'Error loading reports: {str(e)}', 'danger')
        return render_template('attendance/reports.html', classes=[], sections=[])

@attendance_bp.route('/reports/daily')
@require_login
@require_role('admin', 'teacher')
def daily_report():
    """Daily attendance report"""
    try:
        cursor = get_db()
        report_date = request.args.get('date') or datetime.now().strftime('%Y-%m-%d')
        class_id = request.args.get('class_id', type=int)
        section_id = request.args.get('section_id', type=int)
        
        query = """
            SELECT c.class_name, sec.section_name, 
                   COUNT(DISTINCT a.student_id) as total_students,
                   SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) as present_count,
                   SUM(CASE WHEN a.status = 'absent' THEN 1 ELSE 0 END) as absent_count,
                   SUM(CASE WHEN a.status = 'late' THEN 1 ELSE 0 END) as late_count,
                   SUM(CASE WHEN a.status = 'half_day' THEN 1 ELSE 0 END) as half_day_count
            FROM attendance a
            JOIN classes c ON a.class_id = c.id
            JOIN sections sec ON a.section_id = sec.id
            WHERE a.attendance_date = %s
        """
        params = [report_date]
        
        if class_id:
            query += " AND a.class_id = %s"
            params.append(class_id)
        
        if section_id:
            query += " AND a.section_id = %s"
            params.append(section_id)
        
        query += " GROUP BY c.class_name, sec.section_name ORDER BY c.class_name, sec.section_name"
        
        cursor.execute(query, params)
        report_data = cursor.fetchall()
        
        return render_template('attendance/daily_report.html', report_data=report_data, report_date=report_date)
    except Exception as e:
        flash(f'Error generating report: {str(e)}', 'danger')
        return render_template('attendance/daily_report.html', report_data=[], report_date=report_date)

@attendance_bp.route('/reports/class-wise')
@require_login
@require_role('admin', 'teacher')
def class_wise_report():
    """Class-wise attendance report"""
    try:
        cursor = get_db()
        class_id = request.args.get('class_id', type=int)
        section_id = request.args.get('section_id', type=int)
        start_date = request.args.get('start_date') or (datetime.now().replace(day=1)).strftime('%Y-%m-%d')
        end_date = request.args.get('end_date') or datetime.now().strftime('%Y-%m-%d')
        
        if not class_id or not section_id:
            flash('Class and section are required.', 'danger')
            return redirect(url_for('attendance.reports'))
        
        # Get all students in class
        cursor.execute("""
            SELECT s.id, s.admission_number, s.first_name, s.last_name
            FROM students s
            WHERE s.class_id = %s AND s.section_id = %s AND s.is_active = TRUE
            ORDER BY s.first_name, s.last_name
        """, (class_id, section_id))
        students = cursor.fetchall()
        
        # Get attendance for date range
        cursor.execute("""
            SELECT student_id, status, attendance_date
            FROM attendance
            WHERE class_id = %s AND section_id = %s 
            AND attendance_date BETWEEN %s AND %s
        """, (class_id, section_id, start_date, end_date))
        attendance_data = cursor.fetchall()
        
        # Calculate statistics per student
        student_stats = {}
        for student_id, admission_number, first_name, last_name in students:
            student_stats[student_id] = {
                'name': f'{first_name} {last_name}',
                'admission_number': admission_number,
                'total_days': 0,
                'present': 0,
                'absent': 0,
                'late': 0,
                'half_day': 0,
                'percentage': 0
            }
        
        # Process attendance data
        for student_id, status, attendance_date in attendance_data:
            if student_id in student_stats:
                student_stats[student_id]['total_days'] += 1
                if status == 'present':
                    student_stats[student_id]['present'] += 1
                elif status == 'absent':
                    student_stats[student_id]['absent'] += 1
                elif status == 'late':
                    student_stats[student_id]['late'] += 1
                elif status == 'half_day':
                    student_stats[student_id]['half_day'] += 1
        
        # Calculate percentages
        for student_id in student_stats:
            total = student_stats[student_id]['total_days']
            present = student_stats[student_id]['present']
            student_stats[student_id]['percentage'] = (present / total * 100) if total > 0 else 0
        
        cursor.execute("SELECT class_name FROM classes WHERE id = %s", (class_id,))
        class_result = cursor.fetchone()
        class_name = class_result[0] if class_result else 'Unknown'
        
        cursor.execute("SELECT section_name FROM sections WHERE id = %s", (section_id,))
        section_result = cursor.fetchone()
        section_name = section_result[0] if section_result else 'Unknown'
        
        return render_template('attendance/class_wise_report.html',
                             student_stats=list(student_stats.values()),
                             class_name=class_name,
                             section_name=section_name,
                             start_date=start_date,
                             end_date=end_date)
    except Exception as e:
        flash(f'Error generating report: {str(e)}', 'danger')
        return redirect(url_for('attendance.reports'))

@attendance_bp.route('/reports/student/<int:student_id>')
@require_login
def student_report(student_id):
    """Individual student attendance report"""
    try:
        cursor = get_db()
        user_role = session.get('role')
        user_id = session.get('user_id')
        
        # Check access - students can only view their own report
        if user_role == 'student':
            cursor.execute("SELECT id FROM students WHERE user_id = %s", (user_id,))
            student = cursor.fetchone()
            if not student or student[0] != student_id:
                flash('You can only view your own attendance report.', 'danger')
                return redirect(url_for('student.dashboard'))
        
        start_date = request.args.get('start_date') or (datetime.now().replace(day=1)).strftime('%Y-%m-%d')
        end_date = request.args.get('end_date') or datetime.now().strftime('%Y-%m-%d')
        
        # Get student info
        cursor.execute("""
            SELECT s.admission_number, s.first_name, s.last_name, c.class_name, sec.section_name
            FROM students s
            LEFT JOIN classes c ON s.class_id = c.id
            LEFT JOIN sections sec ON s.section_id = sec.id
            WHERE s.id = %s
        """, (student_id,))
        student_info = cursor.fetchone()
        
        if not student_info:
            flash('Student not found.', 'danger')
            return redirect(url_for('attendance.reports'))
        
        # Get attendance records
        cursor.execute("""
            SELECT attendance_date, status, remarks, subject_id, s.subject_name
            FROM attendance a
            LEFT JOIN subjects s ON a.subject_id = s.id
            WHERE a.student_id = %s AND a.attendance_date BETWEEN %s AND %s
            ORDER BY a.attendance_date DESC
        """, (student_id, start_date, end_date))
        attendance_records = cursor.fetchall()
        
        # Calculate statistics
        total_days = len(attendance_records)
        present_count = sum(1 for record in attendance_records if record[1] == 'present')
        absent_count = sum(1 for record in attendance_records if record[1] == 'absent')
        late_count = sum(1 for record in attendance_records if record[1] == 'late')
        half_day_count = sum(1 for record in attendance_records if record[1] == 'half_day')
        percentage = (present_count / total_days * 100) if total_days > 0 else 0
        
        return render_template('attendance/student_report.html',
                             student_info=student_info,
                             attendance_records=attendance_records,
                             total_days=total_days,
                             present_count=present_count,
                             absent_count=absent_count,
                             late_count=late_count,
                             half_day_count=half_day_count,
                             percentage=round(percentage, 2),
                             start_date=start_date,
                             end_date=end_date)
    except Exception as e:
        flash(f'Error generating report: {str(e)}', 'danger')
        return redirect(url_for('attendance.reports'))
