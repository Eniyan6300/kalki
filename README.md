# Quiz Master App 📚

A complete online quiz application built with **Flask** and **SQLite** database. Supports three user roles: Admin, Teacher, and Student with full authentication, quiz creation, question management, and result tracking.

## Features ✨

### Admin Features
- 🔐 Pre-defined admin account (admin@gmail.com / admin123)
- 👥 Manage all users in the system
- 📊 View platform statistics
- 🗑️ Delete users

### Teacher Features
- ✏️ Create and edit quizzes
- ❓ Add multiple types of questions:
  - Multiple Choice Questions (MCQ)
  - True/False questions
  - Short Answer questions
- 📤 Publish quizzes for students
- 📊 View student submissions and results
- 📈 Analytics for quiz performance

### Student Features
- 📝 Attend quizzes
- 💾 Submit quiz answers
- 📊 View personal results and scores
- 🎯 Track quiz performance
- 📈 Grade calculation (A, B, C, D, F)

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite3
- **Frontend**: HTML5, Bootstrap 5, CSS3
- **Password Hashing**: Werkzeug
- **ORM**: SQLAlchemy

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Windows/Mac/Linux

### Step 1: Clone/Download the Project
```bash
cd c:\Users\Admin\Desktop\kalki
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

The app will start on `http://localhost:5000`

## Default Credentials

### Admin Account
- **Email**: admin@gmail.com
- **Password**: admin123

### Create New Accounts
- Teachers and Students can register through the Register page
- Only Teachers and Students can self-register
- Admin account is pre-defined

## Project Structure

```
kalki/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── controller/
│   ├── __init__.py
│   ├── database.py            # Database initialization
│   ├── models.py              # Database models
│   ├── admin_routes.py        # Admin specific routes (can be created)
│   ├── teacher_routes.py      # Teacher specific routes (can be created)
│   ├── student_routes.py      # Student specific routes (can be created)
│   ├── auth_routes.py         # Authentication routes (can be created)
│   └── __pycache__/
│
├── templates/
│   ├── base.html              # Base template
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── admin_dashboard.html   # Admin dashboard
│   ├── admin_users.html       # User management page
│   ├── teacher_dashboard.html # Teacher dashboard
│   ├── create_quiz.html       # Create quiz form
│   ├── edit_quiz.html         # Edit quiz form
│   ├── add_question.html      # Add question form
│   ├── quiz_results.html      # Quiz results (teacher view)
│   ├── student_dashboard.html # Student dashboard
│   ├── take_quiz.html         # Quiz interface for students
│   ├── student_results.html   # Student results page
│   ├── 404.html               # 404 error page
│   └── 500.html               # 500 error page
│
├── static/
│   ├── css/
│   │   ├── style.css          # Custom CSS styling
│   │   └── js/
│   │       └── (JavaScript files)
│   └── ...
│
├── instance/                   # Database storage
│   └── site.db               # SQLite database
│
└── __pycache__/
```

## Database Models

### User Model
- id (Primary Key)
- username (Unique)
- email (Unique)
- password (Hashed)
- created_at (Timestamp)
- roles (Relationship with Role)

### Role Model
- id (Primary Key)
- rolename (Admin, Teacher, Student)

### Quiz Model
- id (Primary Key)
- title
- description
- teacher_id (Foreign Key)
- duration_minutes
- total_marks
- is_published
- created_at, updated_at

### Question Model
- id (Primary Key)
- quiz_id (Foreign Key)
- question_text
- question_type (mcq, true_false, short_answer)
- marks
- options (Relationship with Option)

### Option Model
- id (Primary Key)
- question_id (Foreign Key)
- option_text
- is_correct

### QuizSubmission Model
- id (Primary Key)
- quiz_id (Foreign Key)
- student_id (Foreign Key)
- score
- total_marks
- submitted_at

### StudentAnswer Model
- id (Primary Key)
- quiz_id (Foreign Key)
- question_id (Foreign Key)
- student_id (Foreign Key)
- answer_text
- is_correct
- marks_obtained

## Usage Guide

### For Admins
1. Login with admin@gmail.com / admin123
2. View dashboard statistics
3. Manage users (view and delete)
4. Monitor platform activity

### For Teachers
1. Register as a Teacher
2. Create quizzes from dashboard
3. Add questions (MCQ, True/False, or Short Answer)
4. Publish quizzes to make them available
5. View student submissions and results
6. Analyze quiz performance

### For Students
1. Register as a Student
2. View available quizzes on dashboard
3. Click "Start Quiz" to begin
4. Answer all questions
5. Submit quiz
6. View your results and scores
7. Track your performance over time

## Features Explanation

### Quiz Types
- **MCQ**: Multiple choice questions with one correct answer
- **True/False**: Boolean questions
- **Short Answer**: Text-based answers (manually graded by teacher)

### Grading System
- Automatic grading for MCQ and True/False
- Manual grading option for Short Answer questions
- Grade calculation (A, B, C, D, F based on percentage)

### Password Security
- Passwords are hashed using Werkzeug security
- Never stored in plain text
- Secure login with validation

## API Routes

### Authentication
- `GET /` - Home (redirects to dashboard)
- `GET/POST /login` - User login
- `GET/POST /register` - User registration
- `GET /logout` - User logout

### Admin Routes
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/users` - List all users
- `POST /admin/delete-user/<user_id>` - Delete user

### Teacher Routes
- `GET /teacher/dashboard` - Teacher dashboard
- `GET/POST /teacher/quiz/create` - Create new quiz
- `GET/POST /teacher/quiz/<quiz_id>/edit` - Edit quiz
- `GET/POST /teacher/quiz/<quiz_id>/add-question` - Add question
- `POST /teacher/quiz/<quiz_id>/publish` - Publish quiz
- `POST /teacher/quiz/<quiz_id>/delete` - Delete quiz
- `POST /teacher/question/<question_id>/delete` - Delete question
- `GET /teacher/quiz/<quiz_id>/results` - View results

### Student Routes
- `GET /student/dashboard` - Student dashboard
- `GET /student/quiz/<quiz_id>/start` - Start quiz
- `POST /student/quiz/<quiz_id>/submit` - Submit quiz
- `GET /student/results` - View my results

## Troubleshooting

### Issue: "Module not found" error
**Solution**: Install all required packages:
```bash
pip install -r requirements.txt
```

### Issue: Database errors
**Solution**: Delete the `instance/site.db` file and restart the app to reinitialize:
```bash
rm instance/site.db
python app.py
```

### Issue: Password comparison fails
**Solution**: Ensure passwords are being hashed correctly. Check that the `set_password()` method is being used.

### Issue: Quiz not showing for students
**Solution**: Make sure the quiz is published. Teachers must click "Publish" before students can see it.

## Future Enhancements

- [ ] Email notifications for quiz submissions
- [ ] Question bank management
- [ ] Quiz scheduling
- [ ] Partial marking for short answers
- [ ] Question randomization
- [ ] Answer shuffling for MCQ
- [ ] Time-based quiz locking
- [ ] Detailed analytics and reports
- [ ] Mobile-responsive improvements
- [ ] Dark mode support

## Security Features

- ✅ Session-based authentication
- ✅ Password hashing with Werkzeug
- ✅ Role-based access control (RBAC)
- ✅ CSRF protection (with Flask-WTF optional)
- ✅ Input validation
- ✅ SQL injection prevention (SQLAlchemy ORM)

## Contributing

Feel free to fork and submit pull requests for any improvements.

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please create an issue in the repository.

---

**Built with ❤️ for educational purposes**

