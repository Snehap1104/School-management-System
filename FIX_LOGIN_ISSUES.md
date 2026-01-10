# 🔧 Fix Login Issues - Troubleshooting Guide

## ✅ VERIFIED - Database is OK
- ✓ Admin user exists in database
- ✓ Password hash is correct
- ✓ Password 'admin123' works correctly
- ✓ Database connection is working

## 🔍 Common Login Issues & Solutions

### Issue 1: "Invalid username or password" Error

**Possible Causes:**
1. Wrong username or password
2. User is inactive (is_active = 0)
3. Session not being saved
4. SECRET_KEY issue

**Solutions:**

**A. Verify credentials:**
- Username: `admin` (exactly, no spaces)
- Password: `admin123` (exactly, case-sensitive)

**B. Reset admin password:**
```powershell
py init_db.py
```

**C. Check if user is active:**
Run: `py check_login.py` and verify "Active: 1"

**D. Check SECRET_KEY:**
Make sure `config.py` has a proper SECRET_KEY:
```python
SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
```

### Issue 2: Page Refreshes But Doesn't Login

**Possible Causes:**
1. JavaScript errors
2. Form not submitting
3. CSRF token issue (if enabled)
4. Session not persisting

**Solutions:**

**A. Check browser console:**
- Press F12 → Console tab
- Look for any JavaScript errors

**B. Verify form is submitting:**
- Check Network tab in browser (F12)
- Verify POST request to `/auth/login` is sent

**C. Clear browser cache:**
- Press Ctrl+Shift+Delete
- Clear cookies and cache

**D. Try in incognito/private mode:**
- This rules out browser extension issues

### Issue 3: Redirects Back to Login Page

**Possible Causes:**
1. Session not being set
2. Redirect URL issue
3. Blueprint routing issue

**Solutions:**

**A. Check session in browser:**
- F12 → Application/Storage → Cookies
- Should see `session` cookie after login attempt

**B. Check if admin dashboard exists:**
- Try accessing: http://localhost:5000/admin/dashboard directly
- Should redirect to login if not authenticated

**C. Verify Blueprint registration:**
- Check `app.py` line 31: `app.register_blueprint(auth_bp)`
- Check `app.py` line 32: `app.register_blueprint(admin_bp)`

### Issue 4: No Error Message Showing

**Possible Causes:**
1. Flash messages not rendering
2. Template issue
3. JavaScript hiding messages

**Solutions:**

**A. Check flash messages in template:**
- Verify `templates/base.html` has flash message block
- Check `templates/auth/login.html` extends base.html

**B. Check browser console:**
- Look for template rendering errors

### Issue 5: "Internal Server Error" (500)

**Possible Causes:**
1. Database connection error
2. Missing import
3. Template error
4. Exception in code

**Solutions:**

**A. Check terminal/console output:**
- Look for error traceback
- Common: "Can't connect to MySQL server"

**B. Verify database connection:**
- Check MySQL is running
- Verify password in `config.py` is correct
- Test: `py check_login.py`

**C. Check all imports:**
```powershell
py -c "from app import create_app; app = create_app(); print('OK')"
```

## 🔍 Step-by-Step Debugging

### Step 1: Verify Database
```powershell
py check_login.py
```
Expected output:
- [OK] Admin user found
- [OK] Password 'admin123' is CORRECT
- [OK] Users table exists

### Step 2: Test Database Connection
```powershell
py -c "from config import Config; from database import init_db; from flask import Flask; app = Flask(__name__); app.config.from_object(Config); init_db(app); print('DB OK')"
```

### Step 3: Test App Creation
```powershell
py -c "from app import create_app; app = create_app(); print('App OK')"
```

### Step 4: Run Application with Debug
```powershell
py app.py
```
Watch for any errors in terminal

### Step 5: Test Login in Browser
1. Open: http://localhost:5000
2. Open Developer Tools (F12)
3. Go to Network tab
4. Try to login with: admin / admin123
5. Check:
   - POST request to `/auth/login`
   - Response status (should be 302 redirect)
   - Response headers (should have Set-Cookie for session)
   - Console for JavaScript errors

## 🎯 Quick Fixes to Try

### Fix 1: Reset Everything
```powershell
# 1. Reset admin password
py init_db.py

# 2. Clear browser cache/cookies
# 3. Restart app
py app.py
```

### Fix 2: Check Browser Compatibility
- Try different browser (Chrome, Firefox, Edge)
- Try incognito/private mode
- Disable browser extensions

### Fix 3: Verify Files
```powershell
# Check if all files exist
dir *.py
dir templates\auth\*.html
dir templates\base.html
```

### Fix 4: Check Port
If port 5000 is busy:
```python
# Edit app.py line 58
app.run(debug=True, host='0.0.0.0', port=5001)
```
Then access: http://localhost:5001

## 📋 Login Checklist

Before trying to login, verify:

- [ ] Application is running (`py app.py`)
- [ ] No errors in terminal
- [ ] Browser shows login page at http://localhost:5000
- [ ] Database is accessible (`py check_login.py`)
- [ ] Admin user exists and is active
- [ ] Password hash is correct
- [ ] MySQL password is correct in `config.py`
- [ ] All dependencies installed (`py -m pip list`)
- [ ] Browser console shows no errors (F12)

## 🆘 Still Not Working?

If login still doesn't work:

1. **Check terminal output** when running `py app.py`
   - Look for error messages
   - Share the error message

2. **Check browser console** (F12)
   - Look for JavaScript errors
   - Check Network tab for failed requests

3. **Verify exact error message**
   - What message do you see on screen?
   - Does it show "Invalid username or password"?
   - Does it just refresh the page?
   - Is there an error page?

4. **Share the following:**
   - Terminal output from `py app.py`
   - Browser console errors (F12)
   - What happens when you click "Sign In"
   - Any error messages on screen

## ✅ Expected Working Flow

1. Open http://localhost:5000
2. See login page with username/password fields
3. Enter: `admin` / `admin123`
4. Click "Sign In"
5. Should redirect to admin dashboard
6. Should see "Welcome back, admin!" message
7. Should see admin dashboard with statistics

---

**Run these commands to verify everything:**
```powershell
py check_login.py          # Check database
py -c "from app import create_app; app = create_app(); print('App OK')"  # Test app
py app.py                  # Run app
```
