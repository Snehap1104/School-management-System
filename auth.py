"""
Authentication Blueprint
Handles user login, logout, and session management
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from database import get_db
from utils import require_login, get_current_user

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page and handler"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Username and password are required.', 'danger')
            return render_template('auth/login.html')
        
        try:
            cursor = get_db()
            cursor.execute(
                "SELECT id, username, email, password_hash, role, is_active FROM users WHERE username = %s",
                (username,)
            )
            user = cursor.fetchone()
            
            if user and user[5]:  # Check if user exists and is active
                # Verify password
                if check_password_hash(user[3], password):
                    # Set session
                    session['user_id'] = user[0]
                    session['username'] = user[1]
                    session['email'] = user[2]
                    session['role'] = user[4]
                    
                    flash(f'Welcome back, {user[1]}!', 'success')
                    
                    # Redirect based on role
                    if user[4] == 'admin':
                        return redirect(url_for('admin.dashboard'))
                    elif user[4] == 'teacher':
                        return redirect(url_for('teacher.dashboard'))
                    elif user[4] == 'student':
                        return redirect(url_for('student.dashboard'))
                else:
                    flash('Invalid username or password.', 'danger')
            else:
                flash('Invalid username or password.', 'danger')
        
        except Exception as e:
            flash('An error occurred. Please try again.', 'danger')
            print(f"Login error: {str(e)}")
        
        return render_template('auth/login.html')
    
    # GET request - show login form
    if 'user_id' in session:
        # User already logged in, redirect to dashboard
        role = session.get('role')
        if role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif role == 'teacher':
            return redirect(url_for('teacher.dashboard'))
        elif role == 'student':
            return redirect(url_for('student.dashboard'))
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@require_login
def logout():
    """User logout handler"""
    username = session.get('username', 'User')
    session.clear()
    flash(f'You have been logged out successfully. Goodbye, {username}!', 'info')
    return redirect(url_for('auth.login'))
