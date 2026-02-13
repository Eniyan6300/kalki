# 🔧 Troubleshooting Guide - Quiz Master App

## Common Issues and Solutions

---

## ❌ Issue 1: "ModuleNotFoundError: No module named 'flask'"

### Cause
Flask or other required packages are not installed.

### Solution
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install Flask==3.1.2
pip install Flask-SQLAlchemy==3.1.1
pip install Werkzeug==3.1.5
```

### Verify Installation
```bash
python -c "import flask; print(flask.__version__)"
```

---

## ❌ Issue 2: "Port 5000 already in use"

### Cause
Another application is using port 5000.

### Solution 1: Kill the process using port 5000
```bash
# On Windows (PowerShell as Admin)
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process
```

### Solution 2: Use a different port
Edit the last line of `app.py`:
```python
# Change this:
if __name__ == "__main__":
    app.run(debug=True)

# To this:
if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Use different port
```

---

## ❌ Issue 3: "Database is locked" or "no such column"

### Cause
Database file is corrupted or from an older version.

### Solution
Delete and recreate the database:
```bash
# Navigate to project directory
cd c:\Users\Admin\Desktop\kalki

# Delete the database file
Remove-Item -Path "instance/site.db" -Force

# Restart the app
python app.py
```

---

## ❌ Issue 4: "Admin account not found" or login fails

### Cause
Database wasn't properly initialized.

### Solution
1. Delete `instance/site.db`
2. Restart the app
3. Let it auto-create the admin account
4. Login with: admin@gmail.com / admin123

---

## ❌ Issue 5: Templates not found or blank pages

### Cause
Templates directory is missing or templates are not in the correct location.

### Solution
Ensure directory structure is correct:
```
kalki/
├── app.py
└── templates/
    ├── base.html
    ├── login.html
    └── ... (all other templates)
```

Verify file exists:
```bash
Test-Path "templates/login.html"
```

---

## ❌ Issue 6: CSS styling not loading

### Cause
Static files path is incorrect or CSS file is missing.

### Solution
1. Verify CSS file exists:
   ```
   kalki/static/css/style.css
   ```

2. Hard refresh browser:
   - Press `Ctrl + Shift + Delete` (Windows)
   - Or `Cmd + Shift + Delete` (Mac)
   - Clear cache and reload

3. Check browser console for 404 errors

---

## ❌ Issue 7: "Error 404 Not Found"

### Cause
Route doesn't exist or there's a typo in the URL.

### Solution
1. Verify you're on correct URL: `http://localhost:5000`
2. Check terminal for routing errors
3. Ensure all routes are defined in `app.py`

---

## ❌ Issue 8: Can't login with correct password

### Cause
Password is incorrect or database is corrupted.

### Solution 1: Verify credentials
Default admin:
- Email: `admin@gmail.com`
- Password: `admin123`

### Solution 2: Reset database
```bash
Remove-Item "instance/site.db" -Force
python app.py
# Let it auto-create admin
```

---

## ❌ Issue 9: Questions not showing in quiz

### Cause
Quiz is in draft state or has no questions attached.

### Solution
1. Go to edit quiz
2. Add questions (minimum 1 required)
3. Publish the quiz
4. Students will see it on their dashboard

---

## ❌ Issue 10: Student can't see quizzes

### Cause
Quizzes are not published yet.

### Solution
As a teacher:
1. Login as teacher
2. Go to dashboard
3. Click "Edit" on quiz
4. Click "Publish" button
5. Now students will see it

---

## ❌ Issue 11: Python version error

### Cause
Python version is too old.

### Solution
Check Python version:
```bash
python --version
```

Requires: **Python 3.8 or higher**

If older, download latest from [python.org](https://www.python.org)

---

## ❌ Issue 12: Permission denied errors

### Cause
Running with insufficient permissions.

### Solution

**On Windows:**
- Run Command Prompt as Administrator

**On Mac/Linux:**
- May need `sudo` for system-wide installation:
  ```bash
  sudo pip install -r requirements.txt
  ```

---

## ❌ Issue 13: Virtual environment issues

### Cause
Virtual environment is not activated or corrupted.

### Solution
Recreate virtual environment:
```bash
# Delete old venv
Remove-Item ".venv" -Recurse -Force

# Create new venv
python -m venv .venv

# Activate it
.venv/Scripts/Activate.ps1

# Install requirements
pip install -r requirements.txt
```

---

## ❌ Issue 14: "CORS error" or "origin not allowed"

### Cause
Usually not an issue in development, but if it occurs:

### Solution
Add to `app.py` after Flask initialization:
```python
from flask_cors import CORS
CORS(app)
```

Then install:
```bash
pip install flask-cors
```

---

## ❌ Issue 15: Changes not reflecting after restart

### Cause
Debug mode cache or static files cache.

### Solution
1. Stop the server (Ctrl + C)
2. Clear browser cache:
   - Press Ctrl + Shift + Delete
   - Clear all cache
3. Restart the server:
   ```bash
   python app.py
   ```

---

## 🔍 Debugging Tips

### Enable Verbose Logging
Add to `app.py` before `app.run()`:
```python
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True)
```

### Check Terminal Output
The terminal shows:
- All database queries
- Request logs
- Errors and exceptions
- Debug messages

### Use Browser DevTools
Press `F12` to open:
- Check Network tab for 404s
- Check Console for JavaScript errors
- Check Application tab for storage/session data

### Test Database Connection
```bash
python -c "from app import db; print('Database OK')"
```

---

## 🆘 Still Having Issues?

### Check These Files:
1. **README.md** - Full documentation
2. **QUICKSTART.md** - Quick setup guide
3. **app.py** - Main application code
4. **config.py** - Configuration settings

### Review Logs:
1. Check terminal output for error messages
2. Check browser console (F12)
3. Check application error pages

### Verify Structure:
```bash
# List all project files
Get-ChildItem -Recurse | Select-Object FullName
```

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] All packages installed (`pip list`)
- [ ] Database file deleted (to force recreation)
- [ ] `instance` folder exists
- [ ] `templates` folder exists with all HTML files
- [ ] `static/css/style.css` exists
- [ ] Port 5000 is free
- [ ] No syntax errors in Python files
- [ ] Running from correct directory
- [ ] Firewall not blocking port 5000

---

## 📞 Quick Reference Commands

| Task | Command |
|------|---------|
| Install packages | `pip install -r requirements.txt` |
| Run app | `python app.py` |
| Check Python version | `python --version` |
| Delete database | `Remove-Item instance/site.db -Force` |
| List installed packages | `pip list` |
| Upgrade pip | `python -m pip install --upgrade pip` |
| Create venv | `python -m venv .venv` |
| Activate venv (Windows) | `.venv/Scripts/Activate.ps1` |
| Deactivate venv | `deactivate` |

---

## 🎯 Most Common Solutions

1. **Database issues**: Delete `instance/site.db` and restart
2. **Package issues**: Run `pip install -r requirements.txt`
3. **Port issues**: Change port to 5001 in `app.py`
4. **Login issues**: Use admin@gmail.com / admin123
5. **Template issues**: Verify `templates` folder exists

---

**If all else fails, start fresh:**
```bash
# Stop the server
# Delete instance/site.db
Remove-Item "instance/site.db" -Force

# Reinstall packages
pip install --upgrade -r requirements.txt

# Restart
python app.py
```

---

**Need more help? Check README.md for complete documentation.**
