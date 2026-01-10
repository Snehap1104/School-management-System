# 👨‍🏫 Teacher Role Guide - School Management System

## ✅ Teacher User Created Successfully!

### 🔐 Login Credentials

**Username:** `teacher`  
**Password:** `teacher123`  
**Email:** `teacher@school.com`  
**Name:** John Smith  
**Employee ID:** EMP001

---

## 🚀 How to Login as Teacher

1. **Start the application:**
   ```powershell
   py app.py
   ```

2. **Open browser:** http://localhost:5000

3. **Login with:**
   - Username: `teacher`
   - Password: `teacher123`

4. **You'll be redirected to:** Teacher Dashboard

---

## 📋 Teacher Features & Capabilities

### 1. **Dashboard** (`/teacher/dashboard`)
- View teacher information
- See assigned classes
- See assigned subjects
- View total notes uploaded
- Quick action buttons

### 2. **Upload Study Notes** (`/notes/upload`)
- Upload study materials (PDF, DOC, DOCX, PPT, PPTX)
- Select subject
- Choose class and section
- Add description
- Files stored securely

**Steps:**
1. Click "Upload Notes" in navigation
2. Fill in form:
   - Title (required)
   - Subject (required)
   - Class (required)
   - Section (optional - leave blank for all sections)
   - File (required)
   - Description (optional)
3. Click "Upload Notes"

### 3. **View My Notes** (`/notes/list`)
- See all notes you've uploaded
- Filter by subject, class, section
- Search notes
- Download notes
- Delete your own notes

### 4. **Mark Attendance** (`/attendance/mark`)
- Mark attendance for assigned classes
- Select class and section
- Choose date
- Mark each student as:
  - Present
  - Absent
  - Late
  - Half-day
- Prevent duplicate entries

**Steps:**
1. Click "Mark Attendance" in navigation
2. Select Class → Section → Date
3. Mark status for each student
4. Click "Save Attendance"

### 5. **View Students** (`/student/list`)
- View all students
- Search students by name or admission number
- Filter by class
- View student details

### 6. **Attendance Reports** (`/attendance/reports`)
- View daily attendance reports
- Generate class-wise reports
- View student attendance percentages

---

## 🔒 Teacher Permissions

### ✅ What Teachers CAN Do:
- ✅ Upload study notes
- ✅ View and download own notes
- ✅ Delete own notes
- ✅ Mark attendance for assigned classes
- ✅ View all students
- ✅ View attendance reports
- ✅ View own dashboard

### ❌ What Teachers CANNOT Do:
- ❌ Create/delete users
- ❌ Manage classes/sections/subjects (Admin only)
- ❌ Delete other teachers' notes
- ❌ Access admin dashboard
- ❌ Assign teachers to classes (Admin only)
- ❌ Create/edit/delete students (Admin/Teacher can view)

---

## 📝 Step-by-Step: Upload Notes

1. **Login as teacher**
2. **Navigate to:** Upload Notes (in navigation menu)
3. **Fill the form:**
   ```
   Title: Chapter 5 - Algebra Notes
   Subject: Mathematics
   Class: Grade 5
   Section: A (or leave blank for all)
   File: [Choose PDF/DOC/DOCX/PPT file]
   Description: Basic algebra concepts
   ```
4. **Click:** Upload Notes
5. **Success!** Note is now available to students

---

## 📝 Step-by-Step: Mark Attendance

1. **Login as teacher**
2. **Navigate to:** Mark Attendance
3. **Select filters:**
   - Class: Grade 5
   - Section: A
   - Date: Today's date
4. **Mark each student:**
   - Click radio button for Present/Absent/Late/Half-day
   - Or use "Mark All Present" / "Mark All Absent" buttons
5. **Click:** Save Attendance
6. **Success!** Attendance is recorded

---

## 🎯 Assigning Teacher to Classes (Admin Task)

**Note:** Only Admin can assign teachers to classes. If you need to be assigned:

1. **Login as Admin** (`admin` / `admin123`)
2. **Go to:** Management → Assign Class Teacher
3. **Select:**
   - Teacher: John Smith (teacher)
   - Class: [Select class]
   - Section: [Select section]
4. **Click:** Assign

---

## 🎯 Assigning Subjects to Teacher (Admin Task)

1. **Login as Admin**
2. **Go to:** Management → Assign Subject
3. **Select:**
   - Teacher: John Smith (teacher)
   - Subject: [Select subject]
   - Class: [Optional]
   - Section: [Optional]
4. **Click:** Assign

---

## 🔍 Troubleshooting

### Issue: "Teacher profile not found"
**Solution:** Make sure teacher record exists in database
```powershell
py create_teacher.py
```

### Issue: Cannot see assigned classes
**Solution:** Admin needs to assign you to classes
- Login as admin
- Go to "Assign Class Teacher"
- Assign teacher to class

### Issue: Cannot upload notes
**Solution:** 
- Check file type (PDF, DOC, DOCX, PPT, PPTX)
- Check file size (max 16MB)
- Verify subject and class are selected

### Issue: Cannot mark attendance
**Solution:**
- Make sure you're assigned to that class
- Check if students exist in that class
- Verify date is correct

---

## 📊 Teacher Dashboard Overview

When you login, you'll see:

1. **Teacher Information Card:**
   - Employee ID
   - Name
   - Phone
   - Email
   - Total Notes Uploaded

2. **Assigned Classes Card:**
   - List of classes you're assigned to
   - Shows class name and section

3. **Assigned Subjects Card:**
   - List of subjects you teach
   - Shows subject name and code
   - Shows which classes (if assigned to specific classes)

4. **Quick Actions:**
   - Upload Notes
   - My Notes
   - Mark Attendance
   - View Students

---

## 🎓 Example Workflow

**Daily Routine:**
1. Login → Teacher Dashboard
2. Mark Attendance → Select class → Mark students → Save
3. Upload Notes → Fill form → Upload file → Save
4. View Students → Check student list
5. View Reports → Check attendance statistics

---

## 📞 Need Help?

- **Check:** `README.md` for complete documentation
- **Check:** `FIX_LOGIN_ISSUES.md` for login problems
- **Run:** `py check_login.py` to verify database
- **Run:** `py create_teacher.py` to recreate teacher user

---

**Happy Teaching! 📚**
