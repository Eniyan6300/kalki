# 🚀 QUICK START GUIDE - Quiz Master App

## Installation (First Time Only)

1. **Open Terminal** in the project folder `c:\Users\Admin\Desktop\kalki`

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   This will install Flask, SQLAlchemy, and other required packages.

3. **That's it!** The project is ready to run.

---

## How to Run the App

### Option 1: Run app.py directly (Recommended)
```bash
python app.py
```

### Option 2: Run startup.py (Shows instructions)
```bash
python startup.py
```

### Option 3: Using .venv (Virtual Environment)
```bash
.venv/Scripts/python.exe app.py
```

---

## Access the Application

After starting the server, open your browser and go to:
```
http://localhost:5000
```

---

## Default Admin Login

- **Email**: `admin@gmail.com`
- **Password**: `admin123`

---

## Create Additional Accounts

### Register as Teacher or Student
1. Click "Register" on the login page
2. Enter your details
3. Select role (Teacher or Student)
4. Click Register
5. Login with your credentials

---

## Quick Workflow

### 👨‍🏫 For Teachers:
1. Register → Login
2. Go to Dashboard → Create New Quiz
3. Add questions (MCQ, True/False, Short Answer)
4. Publish quiz
5. Wait for students to submit
6. View results

### 👨‍🎓 For Students:
1. Register → Login
2. See available quizzes on Dashboard
3. Click "Start Quiz" to begin
4. Answer all questions
5. Click "Submit Quiz"
6. View your score and results

### 🔐 For Admin:
1. Login with admin credentials
2. View dashboard statistics
3. Manage users
4. Monitor platform activity

---

## Troubleshooting

### Port 5000 is Already in Use
Change port in `app.py` at the bottom:
```python
app.run(debug=True, host='localhost', port=5001)  # Change 5000 to 5001
```

### Database Issues
Delete the `instance/site.db` file and restart the app:
```bash
rm instance/site.db
python app.py
```

### Module Not Found Error
Reinstall packages:
```bash
pip install --upgrade -r requirements.txt
```

---

## File Structure

```
kalki/
├── app.py                   ← Main application
├── startup.py              ← Easy startup script
├── config.py               ← Configuration
├── requirements.txt        ← Dependencies
├── README.md              ← Full documentation
├── QUICKSTART.md          ← This file
│
├── controller/
│   ├── models.py          ← Database models
│   └── database.py        ← DB initialization
│
├── templates/             ← HTML pages
│   ├── login.html
│   ├── register.html
│   ├── admin_dashboard.html
│   ├── teacher_dashboard.html
│   └── ...
│
└── static/
    └── css/
        └── style.css      ← Styling
```

---

## Key Features

✅ Pre-defined Admin Account
✅ Teacher/Student Self-Registration
✅ Quiz Creation & Management
✅ Multiple Question Types
✅ Automatic Grading
✅ Result Analytics
✅ User Management
✅ Responsive Design

---

## Database

- **Type**: SQLite3
- **Location**: `instance/site.db`
- **Auto-created**: Yes (on first run)
- **Default Tables**: User, Role, Quiz, Question, Option, QuizSubmission, StudentAnswer

---

## Need Help?

1. Check README.md for full documentation
2. Review error messages in terminal
3. Ensure all packages are installed
4. Verify Python version is 3.8+

---

**Ready to use! Happy Testing! 🎉**
