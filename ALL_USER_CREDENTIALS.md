# 🔐 All User Credentials - School Management System

## 📋 Complete List of Test Users

### 1. 👨‍💼 Admin User
- **Username:** `admin`
- **Password:** `admin123`
- **Email:** admin@school.com
- **Role:** Admin
- **Features:** Full system access

**To reset:** `py init_db.py`

---

### 2. 👨‍🏫 Teacher User
- **Username:** `teacher`
- **Password:** `teacher123`
- **Email:** teacher@school.com
- **Name:** John Smith
- **Employee ID:** EMP001
- **Role:** Teacher
- **Features:** Upload notes, mark attendance, view students

**To recreate:** `py create_teacher.py`

---

### 3. 👨‍🎓 Student User
- **Username:** `student`
- **Password:** `student123`
- **Email:** student@school.com
- **Name:** Alice Johnson
- **Admission Number:** ADM20260001
- **Role:** Student
- **Features:** View notes, download materials, view attendance

**To recreate:** `py create_student.py`

---

## 🚀 Quick Login Guide

### Step 1: Start Application
```powershell
py app.py
```

### Step 2: Open Browser
Go to: http://localhost:5000

### Step 3: Login
Use any of the credentials above based on the role you want to test.

---

## 📝 Role-Based Access

### Admin (`admin` / `admin123`)
✅ Full access to all features:
- User management
- Student management
- Teacher management
- Class/Section/Subject management
- Assign teachers to classes
- Assign subjects to teachers
- View all notes
- Mark attendance
- View all reports

### Teacher (`teacher` / `teacher123`)
✅ Teacher-specific features:
- Upload study notes
- View own notes
- Mark attendance
- View students
- View attendance reports
- View dashboard

❌ Cannot:
- Manage users
- Manage classes/subjects
- Delete other teachers' notes
- Access admin features

### Student (`student` / `student123`)
✅ Student-specific features:
- View notes for their class
- Download notes
- View own attendance reports
- View dashboard with statistics

❌ Cannot:
- Upload notes
- Mark attendance
- View other students
- Access admin/teacher features

---

## 🔄 Reset/Recreate Users

### Reset Admin Password
```powershell
py init_db.py
```

### Recreate Teacher User
```powershell
py create_teacher.py
```

### Recreate Student User
```powershell
py create_student.py
```

---

## 📊 Testing Different Roles

### Test Admin Features:
1. Login: `admin` / `admin123`
2. Try: User Management → Add User
3. Try: Management → Classes
4. Try: Students → Add Student

### Test Teacher Features:
1. Login: `teacher` / `teacher123`
2. Try: Upload Notes
3. Try: Mark Attendance
4. Try: View Students

### Test Student Features:
1. Login: `student` / `student123`
2. Try: View Notes
3. Try: Download Notes
4. Try: Attendance Reports

---

## 🎯 Quick Test Checklist

- [ ] Admin login works
- [ ] Teacher login works
- [ ] Student login works
- [ ] Each role sees appropriate dashboard
- [ ] Each role has correct permissions
- [ ] Navigation menu shows correct items for each role

---

**All credentials are ready to use! 🎉**
