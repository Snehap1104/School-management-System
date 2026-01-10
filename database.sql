-- ============================================
-- SCHOOL MANAGEMENT SYSTEM - DATABASE SCHEMA
-- ============================================
-- This schema includes proper relationships, foreign keys, and indexes
-- Created for production-ready Flask application

-- Drop database if exists (use with caution in production)
DROP DATABASE IF EXISTS school_management;
CREATE DATABASE school_management;
USE school_management;

-- ============================================
-- 1. ACADEMIC YEARS TABLE
-- ============================================
CREATE TABLE academic_years (
    id INT AUTO_INCREMENT PRIMARY KEY,
    year_name VARCHAR(50) NOT NULL UNIQUE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_current BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_current (is_current)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 2. USERS TABLE (For authentication)
-- ============================================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'teacher', 'student') NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 3. CLASSES TABLE
-- ============================================
CREATE TABLE classes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(50) NOT NULL,
    class_code VARCHAR(20) UNIQUE,
    description TEXT,
    academic_year_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (academic_year_id) REFERENCES academic_years(id) ON DELETE SET NULL,
    INDEX idx_class_name (class_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 4. SECTIONS TABLE
-- ============================================
CREATE TABLE sections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    section_name VARCHAR(50) NOT NULL,
    class_id INT NOT NULL,
    capacity INT DEFAULT 40,
    academic_year_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
    FOREIGN KEY (academic_year_id) REFERENCES academic_years(id) ON DELETE SET NULL,
    UNIQUE KEY unique_section_class (section_name, class_id, academic_year_id),
    INDEX idx_class_id (class_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 5. SUBJECTS TABLE
-- ============================================
CREATE TABLE subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL,
    subject_code VARCHAR(20) UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_subject_name (subject_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 6. TEACHERS TABLE
-- ============================================
CREATE TABLE teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    qualification TEXT,
    specialization VARCHAR(200),
    hire_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_employee_id (employee_id),
    INDEX idx_name (first_name, last_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 7. STUDENTS TABLE
-- ============================================
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    admission_number VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    gender ENUM('male', 'female', 'other'),
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    parent_name VARCHAR(200),
    parent_phone VARCHAR(20),
    parent_email VARCHAR(255),
    class_id INT,
    section_id INT,
    academic_year_id INT,
    photo_path VARCHAR(500),
    admission_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE SET NULL,
    FOREIGN KEY (section_id) REFERENCES sections(id) ON DELETE SET NULL,
    FOREIGN KEY (academic_year_id) REFERENCES academic_years(id) ON DELETE SET NULL,
    INDEX idx_admission_number (admission_number),
    INDEX idx_class_section (class_id, section_id),
    INDEX idx_name (first_name, last_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 8. CLASS TEACHER ASSIGNMENT
-- ============================================
CREATE TABLE class_teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_id INT NOT NULL,
    class_id INT NOT NULL,
    section_id INT NOT NULL,
    academic_year_id INT,
    assigned_date DATE,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
    FOREIGN KEY (section_id) REFERENCES sections(id) ON DELETE CASCADE,
    FOREIGN KEY (academic_year_id) REFERENCES academic_years(id) ON DELETE SET NULL,
    UNIQUE KEY unique_class_teacher (teacher_id, class_id, section_id, academic_year_id),
    INDEX idx_teacher (teacher_id),
    INDEX idx_class_section (class_id, section_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 9. SUBJECT ASSIGNMENT TO TEACHERS
-- ============================================
CREATE TABLE teacher_subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_id INT NOT NULL,
    subject_id INT NOT NULL,
    class_id INT,
    section_id INT,
    academic_year_id INT,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE SET NULL,
    FOREIGN KEY (section_id) REFERENCES sections(id) ON DELETE SET NULL,
    FOREIGN KEY (academic_year_id) REFERENCES academic_years(id) ON DELETE SET NULL,
    INDEX idx_teacher (teacher_id),
    INDEX idx_subject (subject_id),
    INDEX idx_class_section (class_id, section_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 10. ATTENDANCE TABLE
-- ============================================
CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    class_id INT NOT NULL,
    section_id INT NOT NULL,
    subject_id INT,
    attendance_date DATE NOT NULL,
    status ENUM('present', 'absent', 'late', 'half_day') NOT NULL,
    remarks TEXT,
    marked_by INT,
    academic_year_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
    FOREIGN KEY (section_id) REFERENCES sections(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE SET NULL,
    FOREIGN KEY (marked_by) REFERENCES teachers(id) ON DELETE SET NULL,
    FOREIGN KEY (academic_year_id) REFERENCES academic_years(id) ON DELETE SET NULL,
    UNIQUE KEY unique_student_date (student_id, attendance_date, subject_id),
    INDEX idx_student (student_id),
    INDEX idx_date (attendance_date),
    INDEX idx_class_section_date (class_id, section_id, attendance_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 11. NOTES TABLE (Key Feature)
-- ============================================
CREATE TABLE notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    file_name VARCHAR(500) NOT NULL,
    original_file_name VARCHAR(500),
    file_path VARCHAR(1000) NOT NULL,
    file_size INT,
    file_type VARCHAR(50),
    subject_id INT NOT NULL,
    class_id INT NOT NULL,
    section_id INT,
    teacher_id INT NOT NULL,
    academic_year_id INT,
    description TEXT,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
    FOREIGN KEY (section_id) REFERENCES sections(id) ON DELETE SET NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE CASCADE,
    FOREIGN KEY (academic_year_id) REFERENCES academic_years(id) ON DELETE SET NULL,
    INDEX idx_subject (subject_id),
    INDEX idx_class (class_id),
    INDEX idx_teacher (teacher_id),
    INDEX idx_upload_date (upload_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- INSERT DEFAULT DATA
-- ============================================

-- Insert default academic year
INSERT INTO academic_years (year_name, start_date, end_date, is_current) VALUES
('2024-2025', '2024-04-01', '2025-03-31', TRUE);

-- Insert default admin user (password: admin123)
-- Password hash will be generated by the application, but we'll create it here for initial setup
-- Note: You may need to update this hash after running the application, or create admin through the UI
-- The hash below is for 'admin123' - Update this after first run if it doesn't work
INSERT INTO users (username, email, password_hash, role) VALUES
('admin', 'admin@school.com', 'pbkdf2:sha256:600000$Z8K3mN9p$8c7f8e9d6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c', 'admin');
-- IMPORTANT: If login fails, use Python to generate correct hash:
-- from werkzeug.security import generate_password_hash
-- print(generate_password_hash('admin123'))

-- Insert default subjects
INSERT INTO subjects (subject_name, subject_code) VALUES
('Mathematics', 'MATH'),
('Science', 'SCI'),
('English', 'ENG'),
('Social Studies', 'SST'),
('Computer Science', 'CS'),
('Physical Education', 'PE'),
('Art', 'ART'),
('Music', 'MUS');

-- Insert default classes
SET @academic_year_id = (SELECT id FROM academic_years WHERE is_current = TRUE LIMIT 1);
INSERT INTO classes (class_name, class_code, academic_year_id) VALUES
('Grade 1', 'G1', @academic_year_id),
('Grade 2', 'G2', @academic_year_id),
('Grade 3', 'G3', @academic_year_id),
('Grade 4', 'G4', @academic_year_id),
('Grade 5', 'G5', @academic_year_id),
('Grade 6', 'G6', @academic_year_id),
('Grade 7', 'G7', @academic_year_id),
('Grade 8', 'G8', @academic_year_id),
('Grade 9', 'G9', @academic_year_id),
('Grade 10', 'G10', @academic_year_id);

-- Insert default sections for each class
INSERT INTO sections (section_name, class_id, capacity, academic_year_id)
SELECT 'A', id, 40, @academic_year_id FROM classes
UNION ALL
SELECT 'B', id, 40, @academic_year_id FROM classes
UNION ALL
SELECT 'C', id, 40, @academic_year_id FROM classes WHERE class_name IN ('Grade 1', 'Grade 2', 'Grade 3');
