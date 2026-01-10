# 🔧 Fix Errors When Adding Teacher and Student

## 🐛 Common Errors & Solutions

### Error 1: "Unknown column 'email' in 'field list'" when adding teacher

**Problem:** The `teachers` table doesn't have an `email` column. Email is stored in the `users` table.

**Solution:** Already fixed in `teacher.py`. The INSERT statement no longer includes email for teachers table.

---

### Error 2: "Unknown column 'academic_year' in 'field list'" when adding student

**Problem:** Variable name mismatch in student creation code.

**Solution:** Already fixed in `student.py`. Changed `academic_year` to `academic_year_result`.

---

### Error 3: "Duplicate entry" errors

**Problem:** Trying to add a teacher/student with existing username or employee_id.

**Solution:**
- Use a different username
- Use a different employee ID (for teachers)
- Check existing users first

---

### Error 4: "Table doesn't exist"

**Problem:** Database schema not imported.

**Solution:**
```powershell
mysql -u root -p school_management < database.sql
```

---

### Error 5: "Can't connect to MySQL server"

**Problem:** MySQL not running or wrong credentials.

**Solution:**
1. Check MySQL is running
2. Verify password in `config.py` (line 11)
3. Test connection: `mysql -u root -p`

---

## ✅ Fixed Issues

1. ✅ **Teacher INSERT fixed** - Removed email column from teachers table INSERT
2. ✅ **Student academic_year fixed** - Fixed variable name issue
3. ✅ **Error messages added** - Flash messages now show properly

---

## 🧪 Testing After Fix

### Test Adding Teacher:

1. Login as admin: `admin` / `admin123`
2. Go to: Management → Teachers → Add Teacher
3. Fill form:
   - First Name: Test
   - Last Name: Teacher
   - Employee ID: EMP999 (unique)
   - Username: testteacher (unique)
   - Password: test123
   - (Other fields optional)
4. Click: Save Teacher
5. Should see: "Teacher added successfully!"

### Test Adding Student:

1. Login as admin: `admin` / `admin123`
2. Go to: Students → Add Student
3. Fill form:
   - First Name: Test
   - Last Name: Student
   - Class: [Select a class]
   - Section: [Select a section]
   - (Other fields optional)
4. Click: Save Student
5. Should see: "Student added successfully! Admission Number: ADM2026XXXX"

---

## 🔍 Debugging Steps

If errors still occur:

1. **Check terminal output:**
   ```powershell
   py app.py
   ```
   Look for error messages in terminal

2. **Check browser console:**
   - Press F12
   - Go to Console tab
   - Look for JavaScript errors

3. **Check database:**
   ```powershell
   py check_login.py
   ```

4. **Verify schema:**
   ```sql
   DESCRIBE teachers;
   DESCRIBE students;
   DESCRIBE users;
   ```

---

## 📋 Required Fields Checklist

### For Teacher:
- ✅ First Name (required)
- ✅ Last Name (required)
- ✅ Employee ID (required, must be unique)
- ✅ Username (required, must be unique)
- ✅ Password (required)
- Optional: Phone, Email, Address, Qualification, Specialization, Hire Date

### For Student:
- ✅ First Name (required)
- ✅ Last Name (required)
- Optional: Date of Birth, Gender, Phone, Email, Address, Class, Section, Parent Info, Photo

---

## 🚨 Still Having Issues?

Share the exact error message:
1. What error message appears on screen?
2. What error appears in terminal?
3. Which form are you trying to submit? (Teacher or Student)
4. What fields did you fill?

Then I can provide specific fix!
