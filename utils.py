"""
Utility functions for the application
"""
import os
import uuid
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import session, redirect, url_for, flash, request
from config import Config

def hash_password(password):
    """Hash a password using werkzeug.security"""
    return generate_password_hash(password)

def check_password(password_hash, password):
    """Verify a password against its hash"""
    return check_password_hash(password_hash, password)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def generate_unique_filename(filename):
    """Generate unique filename to prevent overwrites"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    unique_name = f"{uuid.uuid4().hex}.{ext}" if ext else str(uuid.uuid4().hex)
    return unique_name

def secure_file_save(file, folder_path):
    """
    Securely save uploaded file
    Returns: (success: bool, file_path: str or None, error_message: str or None)
    """
    if not file or file.filename == '':
        return False, None, "No file selected"
    
    if not allowed_file(file.filename):
        return False, None, "File type not allowed"
    
    # Create directory if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)
    
    # Generate secure filename
    original_filename = secure_filename(file.filename)
    unique_filename = generate_unique_filename(original_filename)
    file_path = os.path.join(folder_path, unique_filename)
    
    try:
        file.save(file_path)
        return True, file_path, None
    except Exception as e:
        return False, None, f"Error saving file: {str(e)}"

def delete_file(file_path):
    """Delete a file from the server"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        print(f"Error deleting file: {str(e)}")
        return False

def require_login(f):
    """Decorator to require user to be logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def require_role(*roles):
    """Decorator to require specific user role(s)"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))
            
            user_role = session.get('role')
            if user_role not in roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('main.dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_current_user():
    """Get current logged-in user info from session"""
    if 'user_id' not in session:
        return None
    return {
        'user_id': session.get('user_id'),
        'username': session.get('username'),
        'role': session.get('role'),
        'email': session.get('email')
    }
