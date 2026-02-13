from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from config import Config
from controller.database import db
from controller.models import User, Role, Quiz, Question, Option, QuizSubmission, StudentAnswer
from functools import wraps
from datetime import datetime
import json
import socket
from urllib import request as urllib_request
from urllib import error as urllib_error
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# -------------------
# INITIALIZE DATABASE
# -------------------
def init_database():
    with app.app_context():
        db.create_all()

        # Create roles if they don't exist
        roles = ["Admin", "Teacher", "Student"]
        for r in roles:
            if not Role.query.filter_by(rolename=r).first():
                db.session.add(Role(rolename=r))
        db.session.commit()

        # Create predefined admin user
        if not User.query.filter_by(email="admin@gmail.com").first():
            admin_role = Role.query.filter_by(rolename="Admin").first()
            admin = User(username="admin", email="admin@gmail.com")
            admin.set_password("admin123")
            admin.roles.append(admin_role)
            db.session.add(admin)
            db.session.commit()

init_database()


def generate_questions_with_openrouter(
    topic,
    question_type,
    count,
    marks,
    difficulty='medium',
    syllabus_scope='',
    output_language='English'
):
    api_key = app.config.get('OPENROUTER_API_KEY')
    model = app.config.get('OPENROUTER_MODEL')

    if not api_key:
        raise ValueError('OPENROUTER_API_KEY is not configured')

    type_instructions = {
        'mcq': (
            'Generate only MCQ questions. '
            'Each question must have exactly 4 options and one valid correct_option_index (0-3).'
        ),
        'true_false': (
            'Generate only true/false questions. '
            'Set correct_answer strictly as "True" or "False".'
        ),
        'short_answer': (
            'Generate only short answer questions. '
            'Provide a short, clear correct_answer.'
        ),
    }

    system_prompt = (
        'You are a quiz generator for teachers. '
        'Return only valid JSON. No markdown fences. '
        'Output format: {"questions":[...]}'
    )

    user_prompt = (
        f'Topic: {topic}\n'
        f'Question type: {question_type}\n'
        f'Number of questions: {count}\n'
        f'Marks per question: {marks}\n'
        f'Difficulty: {difficulty}\n'
        f'Output language: {output_language}\n'
        f'Syllabus focus: {syllabus_scope or "General conceptual coverage"}\n'
        f'{type_instructions.get(question_type, "")}\n'
        'Each question object must include: '
        '"question_text", "marks", and fields based on type: '
        'MCQ -> "options" (4 strings), "correct_option_index"; '
        'True/False -> "correct_answer"; '
        'Short Answer -> "correct_answer".'
    )

    timeout_seconds = app.config.get('OPENROUTER_TIMEOUT_SECONDS', 25)

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1400,
        "stream": False,
        "response_format": {"type": "json_object"}
    }

    req = urllib_request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib_request.urlopen(req, timeout=timeout_seconds) as response:
            raw = response.read().decode("utf-8")
            result = json.loads(raw)
    except socket.timeout:
        raise ValueError(f"OpenRouter request timed out after {timeout_seconds} seconds")
    except urllib_error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="ignore")
        raise ValueError(f"OpenRouter API error ({e.code}): {error_body}")
    except urllib_error.URLError as e:
        raise ValueError(f"OpenRouter connection error: {e.reason}")
    except Exception as e:
        raise ValueError(f"Unexpected error while calling OpenRouter: {str(e)}")

    try:
        content = result["choices"][0]["message"]["content"]
        data = json.loads(content)
    except Exception:
        raise ValueError("OpenRouter returned an unexpected response format")

    questions = data.get("questions", [])
    if not isinstance(questions, list) or not questions:
        raise ValueError("OpenRouter did not return valid questions")

    return questions


def generate_questions_with_hard_timeout(**kwargs):
    hard_timeout = app.config.get('OPENROUTER_HARD_TIMEOUT_SECONDS', 40)
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(generate_questions_with_openrouter, **kwargs)
        try:
            return future.result(timeout=hard_timeout)
        except FutureTimeoutError:
            raise ValueError(
                f"AI generation exceeded {hard_timeout} seconds. "
                "Please try fewer questions or a shorter topic."
            )

# -------------------
# DECORATORS
# -------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(role_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please login first', 'warning')
                return redirect(url_for('login'))
            
            user = User.query.get(session['user_id'])
            if not user or user.get_role_name() != role_name:
                flash('Access denied', 'danger')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# -------------------
# HOME
# -------------------
@app.route('/')
def index():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        role = user.get_role_name()
        if role == "Admin":
            return redirect(url_for('admin_dashboard'))
        elif role == "Teacher":
            return redirect(url_for('teacher_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))
    return redirect(url_for('login'))

# -------------------
# REGISTER (Teacher & Student only)
# -------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role_name = request.form.get('role')

        # Validate input
        if not all([username, email, password, role_name]):
            flash('All fields are required', 'danger')
            return render_template('register.html')

        if role_name not in ['Teacher', 'Student']:
            flash('Invalid role selection', 'danger')
            return render_template('register.html')

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'warning')
            return render_template('register.html')

        if User.query.filter_by(username=username).first():
            flash('Username already taken', 'warning')
            return render_template('register.html')

        try:
            role = Role.query.filter_by(rolename=role_name).first()
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            new_user.roles.append(role)
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration', 'danger')
            return render_template('register.html')

    return render_template('register.html')

# -------------------
# LOGIN
# -------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Email and password required', 'danger')
            return render_template('login.html')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            role = user.get_role_name()

            flash(f'Welcome {user.username}!', 'success')

            if role == "Admin":
                return redirect(url_for('admin_dashboard'))
            elif role == "Teacher":
                return redirect(url_for('teacher_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))

        flash('Invalid email or password', 'danger')
        return render_template('login.html')

    return render_template('login.html')

# -------------------
# ADMIN ROUTES
# -------------------
@app.route('/admin/dashboard')
@role_required('Admin')
def admin_dashboard():
    total_users = User.query.count() - 1  # Exclude admin
    total_teachers = db.session.query(User).join(User.roles).filter(Role.rolename == 'Teacher').count()
    total_students = db.session.query(User).join(User.roles).filter(Role.rolename == 'Student').count()
    total_quizzes = Quiz.query.count()
    
    users = User.query.all()
    
    return render_template('admin_dashboard.html', 
                         total_users=total_users,
                         total_teachers=total_teachers,
                         total_students=total_students,
                         total_quizzes=total_quizzes,
                         users=users)

@app.route('/admin/users')
@role_required('Admin')
def admin_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/delete-user/<int:user_id>', methods=['POST'])
@role_required('Admin')
def delete_user(user_id):
    if user_id == 1:  # Prevent deletion of admin
        flash('Cannot delete admin user', 'danger')
        return redirect(url_for('admin_users'))
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.username} deleted successfully', 'success')
    return redirect(url_for('admin_users'))

# -------------------
# TEACHER ROUTES
# -------------------
@app.route('/teacher/dashboard')
@role_required('Teacher')
def teacher_dashboard():
    teacher = User.query.get(session['user_id'])
    quizzes = Quiz.query.filter_by(teacher_id=teacher.id).all()
    total_quizzes = len(quizzes)
    total_questions = sum(len(quiz.questions) for quiz in quizzes)
    
    return render_template('teacher_dashboard.html', 
                         quizzes=quizzes,
                         total_quizzes=total_quizzes,
                         total_questions=total_questions)

@app.route('/teacher/quiz/create', methods=['GET', 'POST'])
@role_required('Teacher')
def create_quiz():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        duration_minutes = request.form.get('duration_minutes', 30)
        total_marks = request.form.get('total_marks', 100)
        
        if not title:
            flash('Quiz title is required', 'danger')
            return redirect(url_for('create_quiz'))
        
        quiz = Quiz(
            title=title,
            description=description,
            teacher_id=session['user_id'],
            duration_minutes=int(duration_minutes),
            total_marks=int(total_marks)
        )
        db.session.add(quiz)
        db.session.commit()
        
        flash('Quiz created successfully!', 'success')
        return redirect(url_for('edit_quiz', quiz_id=quiz.id))
    
    return render_template('create_quiz.html')

@app.route('/teacher/quiz/<int:quiz_id>/edit', methods=['GET', 'POST'])
@role_required('Teacher')
def edit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    if quiz.teacher_id != session['user_id']:
        flash('You do not have permission to edit this quiz', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    if request.method == 'POST':
        quiz.title = request.form.get('title')
        quiz.description = request.form.get('description')
        quiz.duration_minutes = int(request.form.get('duration_minutes', 30))
        quiz.total_marks = int(request.form.get('total_marks', 100))
        db.session.commit()
        flash('Quiz updated successfully!', 'success')
        return redirect(url_for('edit_quiz', quiz_id=quiz.id))
    
    return render_template('edit_quiz.html', quiz=quiz)

@app.route('/teacher/quiz/<int:quiz_id>/add-question', methods=['GET', 'POST'])
@role_required('Teacher')
def add_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    if quiz.teacher_id != session['user_id']:
        flash('You do not have permission', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    if request.method == 'POST':
        question_text = request.form.get('question_text')
        question_type = request.form.get('question_type')
        marks = int(request.form.get('marks', 1))
        
        if not question_text or not question_type:
            flash('Question text and type are required', 'danger')
            return redirect(url_for('add_question', quiz_id=quiz_id))
        
        question = Question(
            quiz_id=quiz_id,
            question_text=question_text,
            question_type=question_type,
            marks=marks
        )
        
        if question_type == 'mcq':
            options = request.form.getlist('option')
            correct_option = request.form.get('correct_option')
            
            if len(options) < 2:
                flash('At least 2 options required for MCQ', 'danger')
                return redirect(url_for('add_question', quiz_id=quiz_id))
            
            # Validate that a correct option was selected
            if not correct_option:
                flash('Please select which option is correct!', 'danger')
                return redirect(url_for('add_question', quiz_id=quiz_id))
            
            if not correct_option.isdigit() or int(correct_option) >= len(options):
                flash('Invalid correct option selection', 'danger')
                return redirect(url_for('add_question', quiz_id=quiz_id))
            
            correct_option_idx = int(correct_option)
            for i, option_text in enumerate(options):
                option = Option(
                    question=question,
                    option_text=option_text,
                    is_correct=(i == correct_option_idx)
                )
                db.session.add(option)
        
        elif question_type == 'true_false':
            correct_answer = request.form.get('correct_answer')
            if not correct_answer or correct_answer not in ['True', 'False']:
                flash('Please select a valid correct answer (True or False)', 'danger')
                return redirect(url_for('add_question', quiz_id=quiz_id))
            question.correct_answer = correct_answer
            
        elif question_type == 'short_answer':
            correct_answer = request.form.get('correct_answer', '').strip()
            if not correct_answer:
                flash('Please provide a correct answer for the short answer question', 'danger')
                return redirect(url_for('add_question', quiz_id=quiz_id))
            question.correct_answer = correct_answer
        
        db.session.add(question)
        db.session.commit()
        flash('Question added successfully!', 'success')
        return redirect(url_for('edit_quiz', quiz_id=quiz_id))
    
    return render_template('add_question.html', quiz=quiz)


@app.route('/teacher/quiz/<int:quiz_id>/generate-questions-direct', methods=['POST'])
@role_required('Teacher')
def generate_questions(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    if quiz.teacher_id != session['user_id']:
        flash('You do not have permission', 'danger')
        return redirect(url_for('teacher_dashboard'))

    topic = request.form.get('topic', '').strip()
    question_type = request.form.get('question_type')
    marks = request.form.get('marks', 1)
    count = request.form.get('question_count', 5)
    difficulty = request.form.get('difficulty', 'medium')
    output_language = request.form.get('output_language', 'English')
    syllabus_scope = request.form.get('syllabus_scope', '').strip()

    if not topic:
        flash('Heading/Topic is required for AI generation', 'danger')
        return redirect(url_for('add_question', quiz_id=quiz_id))

    if question_type not in ['mcq', 'true_false', 'short_answer']:
        flash('Invalid question type for AI generation', 'danger')
        return redirect(url_for('add_question', quiz_id=quiz_id))

    if difficulty not in ['easy', 'medium', 'hard']:
        flash('Invalid difficulty selected', 'danger')
        return redirect(url_for('add_question', quiz_id=quiz_id))

    if output_language not in ['English', 'Tamil']:
        flash('Invalid language selected', 'danger')
        return redirect(url_for('add_question', quiz_id=quiz_id))

    try:
        marks = int(marks)
        count = int(count)
    except ValueError:
        flash('Marks and question count must be valid numbers', 'danger')
        return redirect(url_for('add_question', quiz_id=quiz_id))

    if marks < 1:
        flash('Marks must be at least 1', 'danger')
        return redirect(url_for('add_question', quiz_id=quiz_id))

    if count < 1 or count > 20:
        flash('Question count must be between 1 and 20', 'danger')
        return redirect(url_for('add_question', quiz_id=quiz_id))

    try:
        generated_questions = generate_questions_with_hard_timeout(
            topic=topic,
            question_type=question_type,
            count=count,
            marks=marks,
            difficulty=difficulty,
            syllabus_scope=syllabus_scope,
            output_language=output_language
        )

        saved_count = 0
        for item in generated_questions:
            question_text = str(item.get('question_text', '')).strip()
            q_marks = item.get('marks', marks)
            try:
                q_marks = int(q_marks)
            except (TypeError, ValueError):
                q_marks = marks

            if not question_text:
                continue

            question = Question(
                quiz_id=quiz_id,
                question_text=question_text,
                question_type=question_type,
                marks=max(1, q_marks)
            )
            db.session.add(question)
            db.session.flush()

            if question_type == 'mcq':
                options = item.get('options', [])
                correct_option_index = item.get('correct_option_index')
                if not isinstance(options, list) or len(options) < 2:
                    db.session.delete(question)
                    continue

                try:
                    correct_option_index = int(correct_option_index)
                except (TypeError, ValueError):
                    db.session.delete(question)
                    continue

                if correct_option_index < 0 or correct_option_index >= len(options):
                    db.session.delete(question)
                    continue

                for idx, option_text in enumerate(options):
                    option_text = str(option_text).strip()
                    if not option_text:
                        option_text = f'Option {idx + 1}'
                    db.session.add(Option(
                        question_id=question.id,
                        option_text=option_text,
                        is_correct=(idx == correct_option_index)
                    ))

            elif question_type in ['true_false', 'short_answer']:
                correct_answer = str(item.get('correct_answer', '')).strip()
                if question_type == 'true_false' and correct_answer not in ['True', 'False']:
                    db.session.delete(question)
                    continue
                if not correct_answer:
                    db.session.delete(question)
                    continue
                question.correct_answer = correct_answer

            saved_count += 1

        if saved_count == 0:
            db.session.rollback()
            flash('AI response received, but no valid questions could be saved', 'warning')
            return redirect(url_for('add_question', quiz_id=quiz_id))

        db.session.commit()
        flash(f'{saved_count} AI-generated question(s) added successfully!', 'success')
        return redirect(url_for('edit_quiz', quiz_id=quiz_id))

    except Exception as e:
        db.session.rollback()
        flash(f'Failed to generate questions: {str(e)}', 'danger')
        return redirect(url_for('add_question', quiz_id=quiz_id))

@app.route('/teacher/quiz/<int:quiz_id>/publish', methods=['POST'])
@role_required('Teacher')
def publish_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    if quiz.teacher_id != session['user_id']:
        flash('Permission denied', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    if not quiz.questions:
        flash('Cannot publish quiz without questions', 'danger')
        return redirect(url_for('edit_quiz', quiz_id=quiz_id))
    
    quiz.is_published = True
    db.session.commit()
    flash('Quiz published successfully!', 'success')
    return redirect(url_for('teacher_dashboard'))

@app.route('/teacher/quiz/<int:quiz_id>/results')
@role_required('Teacher')
def quiz_results(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    if quiz.teacher_id != session['user_id']:
        flash('Permission denied', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    submissions = QuizSubmission.query.filter_by(quiz_id=quiz_id).all()
    return render_template('quiz_results.html', quiz=quiz, submissions=submissions)

@app.route('/teacher/quiz/<int:quiz_id>/delete', methods=['POST'])
@role_required('Teacher')
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    if quiz.teacher_id != session['user_id']:
        flash('Permission denied', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    db.session.delete(quiz)
    db.session.commit()
    flash('Quiz deleted successfully!', 'success')
    return redirect(url_for('teacher_dashboard'))

@app.route('/teacher/question/<int:question_id>/delete', methods=['POST'])
@role_required('Teacher')
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    quiz_id = question.quiz_id
    quiz = Quiz.query.get(quiz_id)
    
    if quiz.teacher_id != session['user_id']:
        flash('Permission denied', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted successfully!', 'success')
    return redirect(url_for('edit_quiz', quiz_id=quiz_id))

# -------------------
# STUDENT ROUTES
# -------------------
@app.route('/student/dashboard')
@role_required('Student')
def student_dashboard():
    student = User.query.get(session['user_id'])
    available_quizzes = Quiz.query.filter_by(is_published=True).all()
    completed_quizzes = QuizSubmission.query.filter_by(student_id=student.id).all()
    completed_quiz_ids = [sub.quiz_id for sub in completed_quizzes]
    
    pending_quizzes = [q for q in available_quizzes if q.id not in completed_quiz_ids]
    
    return render_template('student_dashboard.html', 
                         pending_quizzes=pending_quizzes,
                         completed_quizzes=completed_quizzes)

@app.route('/student/quiz/<int:quiz_id>/start')
@role_required('Student')
def start_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    
    if not quiz.is_published:
        flash('This quiz is not available', 'danger')
        return redirect(url_for('student_dashboard'))
    
    # Check if student already submitted
    existing_submission = QuizSubmission.query.filter_by(
        quiz_id=quiz_id,
        student_id=session['user_id']
    ).first()
    
    if existing_submission:
        flash('You have already submitted this quiz', 'warning')
        return redirect(url_for('student_dashboard'))
    
    return render_template('take_quiz.html', quiz=quiz)

@app.route('/student/quiz/<int:quiz_id>/submit', methods=['POST'])
@role_required('Student')
def submit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    student_id = session['user_id']
    
    # Check for duplicate submission
    existing = QuizSubmission.query.filter_by(quiz_id=quiz_id, student_id=student_id).first()
    if existing:
        flash('Quiz already submitted', 'warning')
        return redirect(url_for('student_dashboard'))
    
    # Calculate score
    score = 0
    total_marks = 0
    
    for question in quiz.questions:
        total_marks += question.marks
        answer_key = f'question_{question.id}'
        
        if question.question_type == 'mcq':
            selected_option_id = request.form.get(answer_key)
            if selected_option_id:
                option = Option.query.get(selected_option_id)
                is_correct = option.is_correct if option else False
                marks = question.marks if is_correct else 0
                score += marks
                
                student_answer = StudentAnswer(
                    quiz_id=quiz_id,
                    question_id=question.id,
                    student_id=student_id,
                    selected_option_id=selected_option_id,
                    is_correct=is_correct,
                    marks_obtained=marks
                )
                db.session.add(student_answer)
        
        elif question.question_type == 'true_false':
            answer = request.form.get(answer_key)
            
            # Validate we have both answer and correct_answer
            if not answer or not question.correct_answer:
                marks = 0
                is_correct = False
            else:
                # Strip and normalize whitespace for comparison
                answer_clean = answer.strip()
                correct_answer_clean = question.correct_answer.strip()
                # Case-sensitive comparison for True/False (they should be exactly "True" or "False")
                is_correct = (answer_clean == correct_answer_clean)
                marks = question.marks if is_correct else 0
            
            score += marks
            
            student_answer = StudentAnswer(
                quiz_id=quiz_id,
                question_id=question.id,
                student_id=student_id,
                answer_text=answer,
                is_correct=is_correct,
                marks_obtained=marks
            )
            db.session.add(student_answer)
        
        elif question.question_type == 'short_answer':
            answer = request.form.get(answer_key)
            # Short answers are manually graded (teacher can mark later)
            # For now, set is_correct to False (pending manual grading)
            student_answer = StudentAnswer(
                quiz_id=quiz_id,
                question_id=question.id,
                student_id=student_id,
                answer_text=answer,
                is_correct=False,
                marks_obtained=0
            )
            db.session.add(student_answer)
    
    # Create submission record
    submission = QuizSubmission(
        quiz_id=quiz_id,
        student_id=student_id,
        score=score,
        total_marks=total_marks
    )
    db.session.add(submission)
    db.session.commit()
    
    flash(f'Quiz submitted! Your score: {score}/{total_marks}', 'success')
    return redirect(url_for('student_dashboard'))

@app.route('/student/results')
@role_required('Student')
def student_results():
    student = User.query.get(session['user_id'])
    submissions = QuizSubmission.query.filter_by(student_id=student.id).all()
    return render_template('student_results.html', submissions=submissions)

# -------------------
# AI QUESTION GENERATION ROUTES
# -------------------
@app.route('/teacher/quiz/<int:quiz_id>/generate-questions', methods=['GET', 'POST'])
@role_required('Teacher')
def generate_questions_page(quiz_id):
    """Show form to generate questions using AI"""
    quiz = Quiz.query.get_or_404(quiz_id)
    
    if quiz.teacher_id != session['user_id']:
        flash('Permission denied', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'ask_count':
            # First step: User entered topic, ask for number of questions
            topic = request.form.get('topic', '').strip()
            if not topic:
                flash('Please enter a topic', 'danger')
                return render_template('generate_questions.html', quiz=quiz, step='topic')
            
            return render_template('generate_questions.html', quiz=quiz, step='count', topic=topic)
        
        elif action == 'generate':
            # Second step: Generate the questions
            topic = request.form.get('topic', '').strip()
            num_questions = request.form.get('num_questions', 0)
            marks_per_question = request.form.get('marks', 1)
            difficulty = request.form.get('difficulty', 'medium')
            output_language = request.form.get('output_language', 'English')
            syllabus_scope = request.form.get('syllabus_scope', '').strip()
            
            if not topic or not num_questions:
                flash('Topic and number of questions required', 'danger')
                return render_template('generate_questions.html', quiz=quiz, step='count', topic=topic)

            if difficulty not in ['easy', 'medium', 'hard']:
                flash('Invalid difficulty selected', 'danger')
                return render_template('generate_questions.html', quiz=quiz, step='count', topic=topic)

            if output_language not in ['English', 'Tamil']:
                flash('Invalid language selected', 'danger')
                return render_template('generate_questions.html', quiz=quiz, step='count', topic=topic)
            
            try:
                num_questions = int(num_questions)
                marks_per_question = int(marks_per_question)
                
                if num_questions < 1 or num_questions > 20:
                    flash('Enter between 1-20 questions', 'danger')
                    return render_template('generate_questions.html', quiz=quiz, step='count', topic=topic)
                
                if marks_per_question < 1 or marks_per_question > 10:
                    flash('Marks per question should be 1-10', 'danger')
                    return render_template('generate_questions.html', quiz=quiz, step='count', topic=topic)
                
                # Generate questions using OpenRouter API
                generated_questions = generate_questions_with_hard_timeout(
                    topic=topic,
                    question_type='mcq',
                    count=num_questions,
                    marks=marks_per_question,
                    difficulty=difficulty,
                    syllabus_scope=syllabus_scope,
                    output_language=output_language
                )
                
                if not generated_questions:
                    flash('Failed to generate questions', 'danger')
                    return render_template('generate_questions.html', quiz=quiz, step='count', topic=topic)
                
                return render_template('generate_questions.html', 
                                     quiz=quiz, 
                                     step='review', 
                                     topic=topic,
                                     questions=generated_questions,
                                     marks=marks_per_question,
                                     difficulty=difficulty,
                                     output_language=output_language,
                                     syllabus_scope=syllabus_scope)
                
            except ValueError as e:
                flash(f'Error: {str(e)}', 'danger')
                return render_template('generate_questions.html', quiz=quiz, step='count', topic=topic)
            except Exception as e:
                flash(f'Error generating questions: {str(e)}', 'danger')
                return render_template('generate_questions.html', quiz=quiz, step='count', topic=topic)
    
    return render_template('generate_questions.html', quiz=quiz, step='topic')


@app.route('/teacher/quiz/<int:quiz_id>/add-generated-questions', methods=['POST'])
@role_required('Teacher')
def add_generated_questions(quiz_id):
    """Add selected generated questions to quiz"""
    quiz = Quiz.query.get_or_404(quiz_id)
    
    if quiz.teacher_id != session['user_id']:
        flash('Permission denied', 'danger')
        return redirect(url_for('teacher_dashboard'))
    
    try:
        questions_data = json.loads(request.form.get('questions', '[]'))
        
        if not questions_data:
            flash('No questions selected', 'warning')
            return redirect(url_for('generate_questions_page', quiz_id=quiz_id))
        
        added_count = 0
        for q_data in questions_data:
            # Create question
            question = Question(
                quiz_id=quiz_id,
                question_text=q_data.get('question_text'),
                question_type='mcq',
                marks=int(q_data.get('marks', 1))
            )
            db.session.add(question)
            db.session.flush()  # Get the question ID
            
            # Add options
            options = q_data.get('options', [])
            correct_idx = int(q_data.get('correct_option_index', 0))
            
            for i, option_text in enumerate(options):
                option = Option(
                    question_id=question.id,
                    option_text=option_text,
                    is_correct=(i == correct_idx)
                )
                db.session.add(option)
            
            added_count += 1
        
        db.session.commit()
        flash(f'Added {added_count} questions to the quiz!', 'success')
        return redirect(url_for('edit_quiz', quiz_id=quiz_id))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding questions: {str(e)}', 'danger')
        return redirect(url_for('generate_questions_page', quiz_id=quiz_id))

# -------------------
# LOGOUT
# -------------------
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

# -------------------
# ERROR HANDLERS
# -------------------
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)

