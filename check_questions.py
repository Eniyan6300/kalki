#!/usr/bin/env python
"""
Script to check for questions with missing or invalid correct answers
Run this to identify any data issues
"""

from app import app
from controller.database import db
from controller.models import Question

with app.app_context():
    print("=" * 60)
    print("CHECKING QUIZ QUESTIONS FOR DATA ISSUES")
    print("=" * 60)
    
    # Check True/False questions
    tf_questions = Question.query.filter_by(question_type='true_false').all()
    print(f"\nTrue/False Questions: {len(tf_questions)}")
    
    missing_answers = [q for q in tf_questions if not q.correct_answer]
    if missing_answers:
        print(f"⚠️  WARNING: {len(missing_answers)} True/False questions have NO correct answer!")
        for q in missing_answers:
            print(f"   - Quiz ID {q.quiz_id}, Question ID {q.id}: '{q.question_text[:50]}...'")
    else:
        print("✅ All True/False questions have correct answers")
    
    invalid_answers = [q for q in tf_questions if q.correct_answer and q.correct_answer.strip() not in ['True', 'False']]
    if invalid_answers:
        print(f"⚠️  WARNING: {len(invalid_answers)} True/False questions have INVALID correct answers!")
        for q in invalid_answers:
            print(f"   - Quiz ID {q.quiz_id}, Question ID {q.id}: correct_answer='{q.correct_answer}'")
    
    # Check Short Answer questions
    sa_questions = Question.query.filter_by(question_type='short_answer').all()
    print(f"\nShort Answer Questions: {len(sa_questions)}")
    
    missing_sa = [q for q in sa_questions if not q.correct_answer]
    if missing_sa:
        print(f"ℹ️  {len(missing_sa)} Short Answer questions have NO reference answer (these require manual grading)")
    else:
        print("✅ All Short Answer questions have reference answers")
    
    # Check MCQ questions
    from controller.models import Option
    mcq_questions = Question.query.filter_by(question_type='mcq').all()
    print(f"\nMCQ Questions: {len(mcq_questions)}")
    
    for q in mcq_questions:
        correct_opts = [o for o in q.options if o.is_correct]
        if not correct_opts:
            print(f"⚠️  Question ID {q.id}: No correct option marked!")
        elif len(correct_opts) > 1:
            print(f"⚠️  Question ID {q.id}: Multiple correct options marked!")
    
    print("\n" + "=" * 60)
    print("RECOMMENDATION:")
    print("If you see warnings above, you need to:")
    print("1. Go to Teacher Dashboard")
    print("2. Click on the affected quiz")
    print("3. Delete and recreate the questions with proper answers")
    print("=" * 60)
