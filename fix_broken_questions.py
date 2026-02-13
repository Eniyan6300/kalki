#!/usr/bin/env python
"""
Script to delete MCQ questions with no correct answer marked
This fixes the broken quiz questions in the database
"""

from app import app
from controller.database import db
from controller.models import Question, StudentAnswer, Option

with app.app_context():
    print("=" * 60)
    print("FIXING BROKEN MCQ QUESTIONS")
    print("=" * 60)
    
    # Find MCQ questions with no correct option
    mcq_questions = Question.query.filter_by(question_type='mcq').all()
    broken_questions = []
    
    for q in mcq_questions:
        correct_opts = [o for o in q.options if o.is_correct]
        if not correct_opts:
            broken_questions.append(q)
    
    if not broken_questions:
        print("✅ No broken MCQ questions found!")
    else:
        print(f"Found {len(broken_questions)} broken MCQ questions:")
        for q in broken_questions:
            print(f"  - ID {q.id}: '{q.question_text[:60]}...'")
        
        # Delete them
        confirm = input(f"\n⚠️  DELETE these {len(broken_questions)} broken questions? (yes/no): ")
        
        if confirm.lower() == 'yes':
            for q in broken_questions:
                # Delete related student answers first
                StudentAnswer.query.filter_by(question_id=q.id).delete()
                
                # Delete options
                Option.query.filter_by(question_id=q.id).delete()
                
                # Delete question
                db.session.delete(q)
            
            db.session.commit()
            print(f"✅ Deleted {len(broken_questions)} broken questions")
            print("\n📝 NEXT STEPS:")
            print("1. Log in as Teacher")
            print("2. Go to the quiz that had broken questions")  
            print("3. Re-add those MCQ questions with proper correct answers marked")
            print("4. Student will be able to retake the quiz")
        else:
            print("Cancelled - no changes made")
    
    print("=" * 60)
