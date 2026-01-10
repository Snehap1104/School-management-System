"""
School Management System - Main Application
Flask application with modular Blueprint architecture
"""
from flask import Flask, render_template
from config import Config
from database import init_db, close_db
from auth import auth_bp
from admin import admin_bp
from student import student_bp
from teacher import teacher_bp
from notes import notes_bp
from attendance import attendance_bp
from main import main_bp
import os

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    init_db(app)
    
    # Create upload directories
    os.makedirs(Config.STUDENT_PHOTOS_FOLDER, exist_ok=True)
    os.makedirs(Config.NOTES_FOLDER, exist_ok=True)
    
    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(attendance_bp)
    
    # Close database connection on request end
    app.teardown_appcontext(close_db)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
