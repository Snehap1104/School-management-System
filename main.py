"""
Main Blueprint for common routes
"""
from flask import Blueprint, render_template, redirect, url_for, session

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page - redirects to login"""
    if 'user_id' in session:
        role = session.get('role')
        if role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif role == 'teacher':
            return redirect(url_for('teacher.dashboard'))
        elif role == 'student':
            return redirect(url_for('student.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
def dashboard():
    """Main dashboard - redirects based on role"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    role = session.get('role')
    if role == 'admin':
        return redirect(url_for('admin.dashboard'))
    elif role == 'teacher':
        return redirect(url_for('teacher.dashboard'))
    elif role == 'student':
        return redirect(url_for('student.dashboard'))
    
    return redirect(url_for('auth.login'))
