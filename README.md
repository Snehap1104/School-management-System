# School Management System (SMS)

A **complete, production-ready School Management System** built with Python Flask and MySQL. This is an **interview-ready** project following best practices and industry standards.

## 📋 Project Overview

A comprehensive web-based School Management System that manages students, teachers, classes, attendance, and study notes. The system features role-based access control with three user roles: Admin, Teacher, and Student.

**Key Features:**
- ✅ Secure authentication with password hashing
- ✅ Role-based access control (Admin, Teacher, Student)
- ✅ Student management with auto-generated admission numbers
- ✅ Teacher management and assignment system
- ✅ Class and section management
- ✅ Notes management with file upload/download (PDF, DOC, DOCX, PPT)
- ✅ Attendance marking and comprehensive reports
- ✅ Student photo upload
- ✅ Academic year management
- ✅ Clean, modular architecture using Flask Blueprints

---

## 🏗️ Architecture

### Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | Flask 3.0.0 |
| **Database** | MySQL 8.0+ |
| **Database Access** | Flask-MySQLdb (cursor-based queries) |
| **Frontend** | HTML5, CSS3, Bootstrap 5.3, Jinja2 |
| **Authentication** | Session-based with Werkzeug password hashing |
| **File Storage** | Local filesystem (configurable) |

### Project Structure

```
school_management_system/
│
├── app.py                 # Main application entry point
├── config.py              # Configuration settings
├── database.py            # Database connection utilities
├── utils.py               # Helper functions and decorators
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
├── database.sql           # Complete database schema
│
├── auth.py                # Authentication Blueprint
├── admin.py               # Admin module Blueprint
├── student.py             # Student management Blueprint
├── teacher.py             # Teacher management Blueprint
├── notes.py               # Notes management Blueprint
├── attendance.py          # Attendance management Blueprint
├── main.py                # Common routes Blueprint
│
├── templates/             # Jinja2 templates
│   ├── base.html          # Base template
│   ├── auth/              # Authentication templates
│   ├── admin/             # Admin templates
│   ├── student/           # Student templates
│   ├── teacher/           # Teacher templates
│   ├── notes/             # Notes templates
│   ├── attendance/        # Attendance templates
│   └── errors/            # Error pages
│
├── static/                # Static files
│   ├── css/               # Custom stylesheets
│   └── js/                # JavaScript files
│
└── uploads/               # Uploaded files
    ├── student_photos/    # Student profile pictures
    └── notes/             # Study notes (PDF, DOC, etc.)
```

### Architecture Pattern

**MVC (Model-View-Controller) Style with Flask Blueprints:**
- **Model**: MySQL database tables with proper relationships
- **View**: Jinja2 templates with Bootstrap UI
- **Controller**: Flask Blueprint modules handling routes and business logic

**Why This Architecture?**
1. **Modularity**: Each feature is separated into its own Blueprint
2. **Scalability**: Easy to add new modules without affecting existing code
3. **Maintainability**: Clear separation of concerns
4. **Reusability**: Decorators and utilities can be shared across modules

---

## 🗄️ Database Design

### Entity-Relationship Overview

```
users (Authentication)
    ├── students (1:1)
    └── teachers (1:1)

classes ──< sections ──< students
    │
    ├──< class_teachers (M:M)
    └──< teacher_subjects (M:M)

subjects ──< notes
    │
    └──< teacher_subjects

students ──< attendance
    │
    └──< notes (via class_id)
```

### Key Tables

1. **users**: Authentication and authorization
2. **students**: Student information with admission numbers
3. **teachers**: Teacher profiles and assignments
4. **classes**: Class structure
5. **sections**: Class sections
6. **subjects**: Subject catalog
7. **notes**: Study materials with file paths
8. **attendance**: Daily attendance records
9. **academic_years**: Academic year management
10. **class_teachers**: Teacher-class assignment (M:M)
11. **teacher_subjects**: Teacher-subject assignment (M:M)

### Database Features

- ✅ Foreign key constraints with CASCADE operations
- ✅ Unique constraints to prevent duplicates
- ✅ Indexes on frequently queried columns
- ✅ Proper data types and field lengths
- ✅ Timestamps for audit trails
- ✅ Soft delete pattern (is_active flags)

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8+
- MySQL 8.0+
- pip (Python package manager)

### Step 1: Clone/Download Project

```bash
cd school_management_system
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure MySQL Database

1. Create MySQL database:
```sql
CREATE DATABASE school_management;
```

2. Update `config.py` or create `.env` file:
```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=school_management
SECRET_KEY=your-secret-key-here
```

### Step 5: Initialize Database

1. Import database schema:
```bash
mysql -u root -p school_management < database.sql
```

2. Initialize admin user:
```bash
python init_db.py
```

This will create the admin user with credentials:
- **Username**: `admin`
- **Password**: `admin123`

### Step 6: Create Upload Directories

```bash
mkdir -p uploads/student_photos
mkdir -p uploads/notes
```

### Step 7: Run Application

```bash
python app.py
```

The application will run on `http://localhost:5000`

---

## 👥 User Roles & Permissions

### 1. Admin
- ✅ Manage all users (CRUD)
- ✅ Manage classes, sections, subjects
- ✅ Assign teachers to classes
- ✅ Assign subjects to teachers
- ✅ View all dashboards and reports
- ✅ Full system access

### 2. Teacher
- ✅ Upload study notes (PDF, DOC, DOCX, PPT)
- ✅ Mark attendance for assigned classes
- ✅ View student lists
- ✅ View own uploaded notes
- ✅ Access attendance reports

### 3. Student
- ✅ View notes for their class
- ✅ Download study materials
- ✅ View own attendance reports
- ✅ Access dashboard with statistics

---

## 🔐 Security Features

1. **Password Hashing**: Using Werkzeug's `pbkdf2:sha256` algorithm
2. **SQL Injection Protection**: Parameterized queries (cursor.execute with %s)
3. **Session Management**: Secure session-based authentication
4. **Role-Based Access Control**: Decorator-based permission checks
5. **Input Validation**: Server-side validation for all inputs
6. **File Upload Security**: 
   - File type validation
   - File size limits (16MB)
   - Unique filename generation
   - Secure filename handling

---

## 📚 Key Modules Explained

### 1. Authentication Module (`auth.py`)

**Features:**
- Login/logout functionality
- Session management
- Password verification using hashing
- Role-based redirects after login

**Security:**
- Passwords never stored in plain text
- Sessions expire on logout
- Protected routes require authentication

### 2. Admin Module (`admin.py`)

**Features:**
- User management (CRUD operations)
- Class and section management
- Subject catalog management
- Dashboard with statistics
- Quick actions for common tasks

### 3. Student Module (`student.py`)

**Features:**
- Student admission with auto-generated admission numbers
- Photo upload functionality
- Student search and filtering
- Class/section assignment
- Parent information tracking

**Admission Number Format:**
- Pattern: `ADM{YYYY}{XXXX}`
- Example: `ADM20240001`, `ADM20240002`

### 4. Teacher Module (`teacher.py`)

**Features:**
- Teacher profile management
- Class teacher assignment
- Subject assignment to teachers
- View assigned classes and subjects

### 5. Notes Module (`notes.py`) ⭐ **Key Feature**

**Features:**
- File upload (PDF, DOC, DOCX, PPT, PPTX)
- Subject-wise and class-wise organization
- Role-based access:
  - Teachers: Upload and manage own notes
  - Students: View and download notes for their class
  - Admin: Full access
- Secure file storage
- Unique filename generation to prevent overwrites

**File Storage:**
- Physical files: `uploads/notes/`
- Metadata: MySQL `notes` table
- Original filename preserved for download

### 6. Attendance Module (`attendance.py`)

**Features:**
- Mark attendance by class and section
- Multiple status types: Present, Absent, Late, Half-day
- Duplicate prevention (one record per student per day)
- Comprehensive reports:
  - Daily attendance report
  - Class-wise attendance report
  - Individual student attendance percentage
  - Date range filtering

**Attendance Percentage Formula:**
```
Percentage = (Present Days / Total Days) × 100
```

---

## 🎯 Why Flask & MySQL?

### Why Flask?

1. **Lightweight & Flexible**: Minimal overhead, full control
2. **Python Ecosystem**: Rich libraries and community support
3. **Blueprint Architecture**: Perfect for modular applications
4. **Jinja2 Templates**: Powerful templating engine
5. **Easy to Learn**: Simple for beginners, powerful for experts
6. **Perfect for Interviews**: Demonstrates understanding of web frameworks

### Why MySQL?

1. **Relational Data**: Complex relationships (classes, sections, students)
2. **ACID Compliance**: Data integrity and consistency
3. **Mature & Stable**: Industry-standard, widely used
4. **Performance**: Indexes and optimized queries
5. **Foreign Keys**: Enforce referential integrity
6. **Interview Relevance**: Most companies use relational databases

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file (optional, for production):

```env
SECRET_KEY=your-secret-key-change-in-production
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=school_management
```

### Configurable Settings (`config.py`)

- `MAX_CONTENT_LENGTH`: Maximum file upload size (default: 16MB)
- `ALLOWED_EXTENSIONS`: File types allowed for upload
- `UPLOAD_FOLDER`: Directory for uploaded files

---

## 📊 Usage Examples

### Adding a Student

1. Admin/Teacher navigates to "Students" → "Add Student"
2. Fill in student information
3. Upload photo (optional)
4. Select class and section
5. System auto-generates admission number
6. Creates user account automatically

### Uploading Notes (Teacher)

1. Teacher navigates to "Upload Notes"
2. Enter title and select subject
3. Choose class (and optionally section)
4. Upload file (PDF, DOC, DOCX, PPT)
5. Add description (optional)
6. File stored securely with unique name

### Marking Attendance (Teacher/Admin)

1. Select class and section
2. Choose date
3. Mark status for each student (Present/Absent/Late/Half-day)
4. System prevents duplicate entries
5. Save attendance record

---

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check MySQL is running
   - Verify credentials in `config.py`
   - Ensure database exists

2. **Import Errors**
   - Activate virtual environment
   - Run `pip install -r requirements.txt`

3. **File Upload Fails**
   - Check `uploads/` directory permissions
   - Verify file size is under limit
   - Ensure file type is allowed

4. **Login Not Working**
   - Run `python init_db.py` to reset admin password
   - Check password hash in database

---

## 🚀 Deployment Considerations

### Production Checklist

- [ ] Change `SECRET_KEY` to a strong random string
- [ ] Use environment variables for sensitive data
- [ ] Set up proper MySQL user with limited permissions
- [ ] Configure file storage (consider cloud storage like S3)
- [ ] Enable HTTPS/SSL
- [ ] Set up proper logging
- [ ] Configure error handling and monitoring
- [ ] Use production WSGI server (Gunicorn/uWSGI)
- [ ] Set up reverse proxy (Nginx)
- [ ] Implement database backups
- [ ] Add rate limiting
- [ ] Enable CORS if needed for API access

---

## 📈 Future Enhancements

1. **Features:**
   - Email notifications
   - SMS alerts for parents
   - Online fee payment integration
   - Exam/grade management
   - Library management
   - Transport management
   - Hostel management
   - Parent portal with login

2. **Technical:**
   - REST API endpoints
   - Mobile app (React Native/Flutter)
   - Real-time notifications (WebSockets)
   - Advanced search with Elasticsearch
   - File storage on cloud (AWS S3, Azure Blob)
   - Caching with Redis
   - Background jobs with Celery

3. **Improvements:**
   - Unit and integration tests
   - API documentation (Swagger)
   - Docker containerization
   - CI/CD pipeline
   - Performance monitoring
   - Enhanced security (2FA, OAuth)

---

## 💼 Interview Q&A

### 1. **Why did you choose Flask over Django?**

**Answer:**
"I chose Flask because this project required flexibility and modularity. Flask's Blueprint architecture perfectly fits our needs for a modular system. Django would have been overkill for this project size, and Flask gives us more control over the structure. Additionally, Flask is lighter, faster for development, and better demonstrates understanding of web framework fundamentals."

### 2. **How did you handle security in this application?**

**Answer:**
"I implemented multiple security layers:
1. **Password Security**: Using Werkzeug's pbkdf2:sha256 hashing algorithm - passwords are never stored in plain text
2. **SQL Injection Protection**: All queries use parameterized statements with cursor.execute() and placeholders
3. **Role-Based Access Control**: Decorator-based permission checks (@require_role) ensure users can only access authorized resources
4. **Session Management**: Secure session handling with secret keys
5. **File Upload Security**: File type validation, size limits, and unique filename generation prevent malicious uploads"

### 3. **Explain the database schema design.**

**Answer:**
"I designed a normalized relational schema with proper relationships:
- **One-to-One**: users → students, users → teachers (each user can be one student OR one teacher)
- **Many-to-One**: students → classes, sections → classes (many students belong to one class)
- **Many-to-Many**: teachers ↔ classes (via class_teachers table), teachers ↔ subjects (via teacher_subjects table)
- **Foreign Keys**: Enforce referential integrity with CASCADE operations
- **Indexes**: Added on frequently queried columns (username, email, class_id, etc.) for performance
- **Soft Deletes**: Used is_active flags instead of hard deletes for data retention"

### 4. **How does the attendance system prevent duplicates?**

**Answer:**
"I implemented a UNIQUE constraint on the combination of (student_id, attendance_date, subject_id) in the database. When attempting to mark attendance, the system first checks if a record exists for that student on that date. If it exists, we show a warning and allow editing instead of creating a duplicate. The database constraint ensures data integrity even if application-level checks are bypassed."

### 5. **How did you handle file uploads securely?**

**Answer:**
"File upload security is handled in multiple layers:
1. **File Type Validation**: Only allowed extensions (PDF, DOC, DOCX, PPT) are accepted
2. **File Size Limits**: Maximum 16MB to prevent DoS attacks
3. **Unique Filename Generation**: Using UUID to prevent filename collisions and overwrites
4. **Secure Filename Handling**: Using werkzeug's secure_filename() to sanitize user input
5. **Storage Path Validation**: Files stored in designated directories outside web root
6. **Role-Based Access**: Students can only download notes for their class; teachers can only delete their own notes"

### 6. **What challenges did you face and how did you solve them?**

**Answer:**
"Key challenges:

1. **Auto-Generating Admission Numbers**: 
   - Challenge: Ensuring uniqueness and proper format
   - Solution: Implemented pattern-based generation (ADM{Year}{Sequence}) with database checks for uniqueness

2. **Preventing Duplicate Attendance**:
   - Challenge: Multiple teachers marking same class, same day
   - Solution: Unique constraint on (student_id, date, subject_id) plus application-level checks

3. **Role-Based File Access**:
   - Challenge: Students should only access their class notes
   - Solution: Implemented role-based decorators and query filtering based on logged-in user's class

4. **Handling Many-to-Many Relationships**:
   - Challenge: Teachers assigned to multiple classes and subjects
   - Solution: Created junction tables (class_teachers, teacher_subjects) with proper foreign keys"

### 7. **How would you scale this application?**

**Answer:**
"Scaling strategies:

1. **Database Level**:
   - Add read replicas for reporting queries
   - Implement database connection pooling
   - Add more indexes based on query patterns
   - Consider partitioning large tables (attendance by year)

2. **Application Level**:
   - Use caching (Redis) for frequently accessed data (class lists, student counts)
   - Implement pagination for large result sets
   - Move file storage to cloud (S3) with CDN
   - Add background job processing (Celery) for heavy operations

3. **Infrastructure**:
   - Deploy with Gunicorn/uWSGI behind Nginx
   - Horizontal scaling with load balancer
   - Use containerization (Docker) for consistency
   - Implement microservices for large features (separate attendance service)

4. **Performance**:
   - Query optimization and N+1 problem prevention
   - Implement lazy loading where appropriate
   - Use async operations for file uploads/downloads
   - Add monitoring and profiling tools"

### 8. **What design patterns did you use?**

**Answer:**
"Several patterns implemented:

1. **Blueprint Pattern**: Modular route organization (each feature is a Blueprint)
2. **Decorator Pattern**: @require_login, @require_role for access control
3. **Factory Pattern**: create_app() function for application factory
4. **MVC Pattern**: Separated models (DB), views (templates), controllers (routes)
5. **Singleton Pattern**: Database connection management (g object in Flask)
6. **Strategy Pattern**: Different behaviors based on user roles"

### 9. **How would you add testing to this project?**

**Answer:**
"I would implement:

1. **Unit Tests** (pytest):
   - Test utility functions (password hashing, file validation)
   - Test decorators (role-based access)
   - Test individual route handlers with mocked database

2. **Integration Tests**:
   - Test complete workflows (student admission, attendance marking)
   - Test database operations end-to-end
   - Test file upload/download functionality

3. **Test Database**:
   - Separate test database
   - Use fixtures for test data
   - Clean up after each test

4. **Coverage**:
   - Aim for 80%+ code coverage
   - Focus on critical paths (authentication, data modification)

Example test structure:
```python
# tests/test_auth.py
def test_login_success(client):
    response = client.post('/auth/login', data={
        'username': 'admin',
        'password': 'admin123'
    })
    assert response.status_code == 302
    assert session.get('user_id') is not None
```"

### 10. **What improvements would you make if you rebuilt this?**

**Answer:**
"If rebuilding, I would:

1. **API-First Approach**: Build RESTful API, then consume it with frontend
2. **Modern Frontend**: React or Vue.js for better UX
3. **Better Validation**: Use Flask-WTF or Pydantic for schema validation
4. **Database ORM**: Consider SQLAlchemy for better abstraction
5. **Testing from Start**: TDD approach with comprehensive test suite
6. **Documentation**: API docs with Swagger/OpenAPI
7. **Logging**: Structured logging with proper log levels
8. **Error Handling**: Custom exception classes and better error messages
9. **Configuration Management**: Use Flask-Config or environment-based config
10. **Code Quality**: Pre-commit hooks, linting (flake8, black), type hints"

---

## 📝 License

This project is created for educational and interview purposes. Feel free to use it as a portfolio project or learning resource.

---

## 👨‍💻 Author

Built as a complete, interview-ready School Management System demonstrating:
- Full-stack development skills
- Database design and optimization
- Security best practices
- Clean code architecture
- Production-ready implementation

---

## 🙏 Acknowledgments

- Flask community for excellent documentation
- Bootstrap for UI components
- MySQL for robust database system

---

**Note**: This is a complete, production-like project suitable for:
- ✅ Resume/Portfolio projects
- ✅ GitHub showcase
- ✅ Technical interviews
- ✅ Learning full-stack development
- ✅ Understanding Flask architecture

**Happy Coding! 🚀**
