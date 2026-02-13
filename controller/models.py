from controller.database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

user_role = db.Table(
    'user_role',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(50), unique=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    roles = db.relationship('Role', secondary=user_role, backref='users')
    quizzes = db.relationship('Quiz', backref='teacher', lazy=True, foreign_keys='Quiz.teacher_id')
    student_answers = db.relationship('StudentAnswer', backref='student', lazy=True)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_role_name(self):
        if self.roles:
            return self.roles[0].rolename
        return None

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    duration_minutes = db.Column(db.Integer, default=30)  # Quiz duration in minutes
    total_marks = db.Column(db.Integer, default=100)
    is_published = db.Column(db.Boolean, default=False)
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade='all, delete-orphan')
    submissions = db.relationship('QuizSubmission', backref='quiz', lazy=True, cascade='all, delete-orphan')

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    marks = db.Column(db.Integer, default=1)
    question_type = db.Column(db.String(20), default='mcq')  # mcq, true_false, short_answer
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    options = db.relationship('Option', backref='question', lazy=True, cascade='all, delete-orphan')
    answers = db.relationship('StudentAnswer', backref='question', lazy=True, cascade='all, delete-orphan')
    correct_answer = db.Column(db.Text)  # For true/false and short answer questions

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    option_text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

class QuizSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Float)
    total_marks = db.Column(db.Float)
    student = db.relationship('User', backref='quiz_submissions')

class StudentAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    answer_text = db.Column(db.Text)
    selected_option_id = db.Column(db.Integer, db.ForeignKey('option.id'))
    is_correct = db.Column(db.Boolean)
    marks_obtained = db.Column(db.Float, default=0)
    quiz = db.relationship('Quiz')
    selected_option = db.relationship('Option')

