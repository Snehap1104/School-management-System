# 🚀 School Management System - Setup & Run Guide

## ✅ Quick Start (Step-by-Step)

### Step 1: Check Python Installation
```powershell
py --version
```
**Expected Output:** Python 3.8 or higher

---

### Step 2: Install Dependencies

**Option A: Install all dependencies (Recommended)**
```powershell
py -m pip install -r requirements.txt
```

**Option B: Install manually**
```powershell
py -m pip install Flask==3.0.0
py -m pip install Flask-MySQLdb==1.0.1
py -m pip install Werkzeug==3.0.1
py -m pip install mysql-connector-python==8.2.0
py -m pip install python-dotenv==1.0.0
py -m pip install Pillow==10.1.0
```

**Verify Installation:**
```powershell
py -m pip list | Select-String -Pattern "Flask"
```

---

### Step 3: Setup MySQL Database

**3.1. Create Database**
```powershell
# Open MySQL command line (if MySQL is installed)
mysql -u root -p
```

Then in MySQL:
```sql
CREATE DATABASE school_management;
exit
```

**3.2. Import Database Schema**
```powershell
# Navigate to project directory (if not already there)
cd C:\Users\SNEHA\school_management_system

# Import schema
mysql -u root -p school_management < database.sql
```

**Alternative: If mysql command not in PATH**
- Use MySQL Workbench or phpMyAdmin
- Open `database.sql` file
- Execute all SQL commands in your MySQL client

---

### Step 4: Configure Database Connection

**Option A: Update config.py directly**
Edit `config.py` and update these lines:
```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_password'  # Change this
MYSQL_DB = 'school_management'
```

**Option B: Create .env file (Recommended for production)**
Create a file named `.env` in the project root:
```env
SECRET_KEY=your-secret-key-here
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=school_management
```

---

### Step 5: Initialize Admin User

```powershell
py init_db.py
```

**Expected Output:**
```
Initializing School Management System Database...
--------------------------------------------------
✓ Admin password updated successfully!
  Username: admin
  Password: admin123

✓ Database initialized successfully!
  You can now login with the admin credentials.
```

---

### Step 6: Create Upload Directories

The application will create these automatically, but you can create them manually:
```powershell
New-Item -ItemType Directory -Force -Path uploads\student_photos
New-Item -ItemType Directory -Force -Path uploads\notes
```

---

### Step 7: Run the Application

```powershell
py app.py
```

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
 * Running on http://0.0.0.0:5000
Press CTRL+C to quit
```

---

### Step 8: Access the Application

Open your web browser and go to:
- **URL:** http://localhost:5000
- **OR:** http://127.0.0.1:5000

**Default Login Credentials:**
- **Username:** `admin`
- **Password:** `admin123`

---

## 🔧 Troubleshooting

### Issue 1: "ModuleNotFoundError: No module named 'Flask'"
**Solution:**
```powershell
py -m pip install Flask
# Or reinstall all dependencies
py -m pip install -r requirements.txt
```

### Issue 2: "Error 2003: Can't connect to MySQL server"
**Solutions:**
1. **Check if MySQL is running:**
   - Windows: Check Services (services.msc) → MySQL
   - Or: Open MySQL Workbench and try connecting

2. **Verify credentials in config.py:**
   - Check MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD

3. **Test MySQL connection manually:**
   ```powershell
   mysql -u root -p
   ```

### Issue 3: "Table 'school_management.users' doesn't exist"
**Solution:**
- Import database schema:
  ```powershell
  mysql -u root -p school_management < database.sql
  ```

### Issue 4: "Permission denied" or "Access denied"
**Solution:**
1. Check MySQL user permissions
2. Grant privileges:
   ```sql
   GRANT ALL PRIVILEGES ON school_management.* TO 'root'@'localhost';
   FLUSH PRIVILEGES;
   ```

### Issue 5: "Port 5000 already in use"
**Solution:**
Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001 or any other port
```

### Issue 6: Import Errors
**Solutions:**
```powershell
# Make sure you're in the project directory
cd C:\Users\SNEHA\school_management_system

# Verify all files exist
dir *.py

# Reinstall dependencies
py -m pip install --upgrade -r requirements.txt
```

---

## 📋 Complete Command Sequence (Copy & Paste)

```powershell
# 1. Navigate to project directory
cd C:\Users\SNEHA\school_management_system

# 2. Install dependencies
py -m pip install -r requirements.txt

# 3. Import database (after creating database in MySQL)
mysql -u root -p school_management < database.sql

# 4. Initialize admin user
py init_db.py

# 5. Run application
py app.py
```

---

## 🎯 Quick Test Checklist

After running the application, verify:

- [ ] Application starts without errors
- [ ] Can access http://localhost:5000
- [ ] Login page appears
- [ ] Can login with admin/admin123
- [ ] Admin dashboard loads
- [ ] Can view users list
- [ ] Can add a student
- [ ] Can upload notes (as teacher)

---

## 🔐 Default Credentials

**Admin:**
- Username: `admin`
- Password: `admin123`

**To reset admin password:**
```powershell
py init_db.py
```

---

## 📝 Notes

1. **Development Server:** The default Flask development server is for development only. For production, use Gunicorn or uWSGI.

2. **Database:** Make sure MySQL service is running before starting the application.

3. **File Uploads:** Files are stored in `uploads/` directory. Make sure this directory has write permissions.

4. **Port:** Default port is 5000. If it's busy, change it in `app.py`.

5. **Debug Mode:** Debug mode is enabled by default. Disable in production!

---

## 🆘 Still Having Issues?

1. Check Python version: `py --version` (should be 3.8+)
2. Check MySQL installation: `mysql --version`
3. Check all files are present: `dir`
4. Check error messages in terminal carefully
5. Verify database schema is imported correctly

---

**Happy Coding! 🚀**
