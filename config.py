import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'root'  # Change this to your MySQL password
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'school_management'
    
    # File upload settings
    UPLOAD_FOLDER = 'uploads'
    STUDENT_PHOTOS_FOLDER = 'uploads/student_photos'
    NOTES_FOLDER = 'uploads/notes'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx', 'png', 'jpg', 'jpeg'}
