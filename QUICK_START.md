# 🚀 Quick Start Guide - School Management System

## ⚡ FASTEST WAY TO RUN (3 Steps)

### **Step 1: Setup Database**

**Option A: If MySQL is already running**
```powershell
# Import database schema
mysql -u root -p school_management < database.sql
```

**Option B: If MySQL command not available**
1. Open MySQL Workbench or phpMyAdmin
2. Create database: `CREATE DATABASE school_management;`
3. Open `database.sql` file
4. Copy and paste all SQL commands into MySQL client
5. Execute all commands

**Step 2: Configure MySQL Password**

Edit `config.py` line 11:
```python
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'your_mysql_password_here'
```
Replace `'your_mysql_password_here'` with your actual MySQL password.

**OR create `.env` file:**
```
MYSQL_PASSWORD=your_mysql_password
```

### **Step 3: Run the Application**

**Option A: Double-click `run.bat` file** (Easiest!)

**Option B: Command Line**
```powershell
py app.py
```

**That's it!** Open http://localhost:5000 in your browser.

---

## 🔐 Default Login

- **Username:** `admin`
- **Password:** `admin123`

**If login fails, run:**
```powershell
py init_db.py
```

---

## ❌ Common Errors & Fixes

### Error: "Can't connect to MySQL server"

**Fix:** 
1. Make sure MySQL is running (check Services on Windows)
2. Update password in `config.py` (line 11)
3. Test connection:
   ```powershell
   mysql -u root -p
   ```

### Error: "Table doesn't exist"

**Fix:**
Import database schema:
```powershell
mysql -u root -p school_management < database.sql
```

### Error: "ModuleNotFoundError"

**Fix:**
```powershell
py -m pip install -r requirements.txt
```

### Error: "Port 5000 already in use"

**Fix:** 
Edit `app.py` last line:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

---

## 📝 Checklist Before Running

- [ ] Python installed (`py --version`)
- [ ] Dependencies installed (`py -m pip list | Select-String Flask`)
- [ ] MySQL installed and running
- [ ] Database `school_management` created
- [ ] Database schema imported (`database.sql`)
- [ ] MySQL password configured in `config.py`
- [ ] Admin user initialized (`py init_db.py`)

---

## 🎯 After Running Successfully

You should see:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

Then:
1. Open browser → http://localhost:5000
2. Login with `admin` / `admin123`
3. Explore the system! 🎉

---

**Need Help?** Check `SETUP_GUIDE.md` for detailed instructions.
