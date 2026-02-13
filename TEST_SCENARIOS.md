# 🧪 Test Scenarios - Quiz Master App

## Complete Testing Guide with Step-by-Step Instructions

---

## Scenario 1: Admin User Login & Dashboard

### Pre-requisites
- Flask app is running
- Browser is open to `http://localhost:5000`

### Steps

1. **Access Login Page**
   - You should be redirected to login page
   - Click on "Login" tab

2. **Enter Admin Credentials**
   - Email: `admin@gmail.com`
   - Password: `admin123`
   - Click "Login"

3. **Verify Admin Dashboard**
   - ✅ Should see "🔐 Admin Dashboard"
   - ✅ Should see statistics cards (Total Users, Teachers, Students, Quizzes)
   - ✅ Should see "Manage Users" button
   - ✅ Should see a table of all users

### Expected Results
- Login successful
- Redirected to admin dashboard
- Statistics displayed correctly
- Users table populated

---

## Scenario 2: Register as Teacher

### Steps

1. **Access Registration Page**
   - Click "Register" link from login page
   - Or go to `http://localhost:5000/register`

2. **Fill Registration Form**
   - Username: `teacher_john`
   - Email: `john.teacher@email.com`
   - Password: `teacher123`
   - Role: Select "Teacher"
   - Click "Register"

3. **Verify Registration**
   - ✅ Should see success message
   - ✅ Should be redirected to login page

4. **Login with Teacher Account**
   - Email: `john.teacher@email.com`
   - Password: `teacher123`
   - Click "Login"

### Expected Results
- Registration successful
- New user created in database
- Login works with new credentials
- Redirected to teacher dashboard

---

## Scenario 3: Teacher Creates Quiz

### Pre-requisites
- Logged in as a teacher
- On teacher dashboard

### Steps

1. **Create Quiz**
   - Click "Create New Quiz" button
   - Fill in form:
     - Quiz Title: "History Quiz 2026"
     - Description: "Basic questions about world history"
     - Duration: 30 minutes
     - Total Marks: 100
   - Click "Create Quiz"

2. **Verify Quiz Created**
   - ✅ Should see success message
   - ✅ Should be on edit quiz page
   - ✅ Quiz should appear in dashboard

### Expected Results
- Quiz created successfully
- Redirected to edit quiz page
- Quiz appears in quizzes list with "Draft" status

---

## Scenario 4: Add MCQ Question

### Pre-requisites
- Logged in as teacher
- Have a created quiz
- On edit quiz page

### Steps

1. **Add Question Button**
   - Click "Add Question" button

2. **Fill Question Form**
   - Question Text: "What is the capital of France?"
   - Question Type: "Multiple Choice (MCQ)"
   - Marks: 5
   - Options:
     - Option 1: "Paris"
     - Option 2: "London"
     - Option 3: "Berlin"
     - Option 4: "Rome"
   - Mark Correct Answer: Select "Paris" (Option 1)
   - Click "Add Question"

3. **Verify Question Added**
   - ✅ Should see success message
   - ✅ Question should appear in quiz questions list
   - ✅ Should see "Options: 4"

### Expected Results
- MCQ question added successfully
- Question appears in quiz
- Question can be seen on edit quiz page

---

## Scenario 5: Add True/False Question

### Steps

1. **Click Add Question**

2. **Fill Form**
   - Question Text: "The Earth revolves around the Sun"
   - Question Type: "True/False"
   - Marks: 3
   - Correct Answer: "True"
   - Click "Add Question"

3. **Verify**
   - ✅ Question added to quiz

### Expected Results
- True/False question added
- Shows as "true_false" type in list

---

## Scenario 6: Add Short Answer Question

### Steps

1. **Click Add Question**

2. **Fill Form**
   - Question Text: "Name any Renaissance artist"
   - Question Type: "Short Answer"
   - Marks: 10
   - Sample Answer: "Leonardo da Vinci"
   - Click "Add Question"

3. **Verify**
   - ✅ Question added

### Expected Results
- Short answer question added
- Marked as "short_answer" type

---

## Scenario 7: Publish Quiz

### Pre-requisites
- Quiz has at least 1 question
- Quiz status is "Draft"

### Steps

1. **Go to Teacher Dashboard**
   - Click "← Back to Dashboard"

2. **Find Quiz**
   - Should see quiz in list with "Draft" badge

3. **Publish Quiz**
   - Click "📤 Publish" button
   - Confirm success message

4. **Verify Published**
   - ✅ Quiz status changes to "Published" (green badge)
   - ✅ "results" button appears
   - ✅ Students can now see this quiz

### Expected Results
- Quiz marked as published
- Badge changes to green
- Quiz visible to students

---

## Scenario 8: Register as Student

### Steps

1. **Logout as Teacher**
   - Click "Logout" in navbar

2. **Register as Student**
   - Click "Register"
   - Fill form:
     - Username: `student_alice`
     - Email: `alice.student@email.com`
     - Password: `student123`
     - Role: "Student"
   - Click "Register"

3. **Login as Student**
   - Email: `alice.student@email.com`
   - Password: `student123`

### Expected Results
- Student account created
- Student logged in successfully
- Redirected to student dashboard

---

## Scenario 9: Student Takes Quiz

### Pre-requisites
- Logged in as student
- Quiz is published by teacher
- On student dashboard

### Steps

1. **View Available Quizzes**
   - ✅ Should see published quiz (History Quiz)

2. **Start Quiz**
   - Click "Start Quiz" button

3. **Answer Questions**
   - **Question 1 (MCQ)**: Select "Paris"
   - **Question 2 (True/False)**: Select "True"
   - **Question 3 (Short Answer)**: Type "Leonardo da Vinci"

4. **Submit Quiz**
   - Scroll to bottom
   - Click "Submit Quiz"
   - Confirm submission

### Expected Results
- Quiz form displayed
- All questions visible
- Questions can be answered
- Quiz submits successfully
- Success message shown
- Redirected to dashboard

---

## Scenario 10: Student Checks Results

### Pre-requisites
- Student has submitted a quiz
- On student dashboard

### Steps

1. **View Results**
   - Click "View My Results" button

2. **Verify Results Page**
   - ✅ Should see submitted quiz in table
   - ✅ Should see score (e.g., 18/25)
   - ✅ Should see percentage (e.g., 72%)
   - ✅ Should see grade letter (e.g., "C")

3. **Check Statistics**
   - ✅ Total Quizzes Taken
   - ✅ Average Score
   - ✅ Best Score

### Expected Results
- Results page displays
- Correct score shown (MCQ + True/False auto-graded)
- Short answer not graded (needs teacher grading)
- Statistics calculated correctly

---

## Scenario 11: Teacher Views Results

### Pre-requisites
- Logged in as teacher
- Student has submitted quiz

### Steps

1. **Go to Teacher Dashboard**
   - Should be logged in as teacher

2. **View Quiz Results**
   - Find quiz in list
   - Click "📊 Results" button

3. **Verify Results Page**
   - ✅ Should see student name "student_alice"
   - ✅ Should see score (18/25)
   - ✅ Should see percentage (72%)
   - ✅ Should see badge with color (red for fail, yellow for pass, green for high score)

4. **Check Statistics**
   - ✅ Total Submissions: 1
   - ✅ Average Score: 18
   - ✅ Highest Score: 18
   - ✅ Lowest Score: 18

### Expected Results
- Results displayed correctly
- Submissions table populated
- Statistics calculated accurately

---

## Scenario 12: Admin Deletes User

### Pre-requisites
- Logged in as admin
- Multiple users exist

### Steps

1. **Go to Manage Users**
   - Click "Manage Users" or go to admin/users

2. **View User List**
   - ✅ Should see all teachers and students
   - ✅ Should see delete button for each user

3. **Delete a User**
   - Find a student (e.g., student_alice)
   - Click "Delete" button
   - Confirm in popup

4. **Verify Deletion**
   - ✅ User removed from list
   - ✅ Success message displayed

### Expected Results
- User deleted successfully
- No longer in users list
- Cannot login with deleted user

---

## Scenario 13: Test Error Handling

### Invalid Login
```
Email: invalid@email.com
Password: wrongpassword
Expected: "Invalid email or password" message
```

### Duplicate Email Registration
```
Try registering with same email as existing user
Expected: "Email already registered" message
```

### Missing Required Fields
```
Try submitting form with empty fields
Expected: Validation error message
```

### Delete Non-Existent Quiz
```
Try accessing /teacher/quiz/9999/delete
Expected: 404 error page
```

---

## Scenario 14: Database & Performance Testing

### Create Multiple Quizzes
1. Create 5 different quizzes
2. Add 10+ questions each
3. Verify all load correctly

### Create Multiple Students
1. Register 10+ student accounts
2. Have different students take different quizzes
3. Verify results tracked correctly

### Verify Database
- Check `instance/site.db` exists
- File size increases as data added
- Database persists across restarts

---

## Scenario 15: UI & Responsiveness Testing

### Desktop Testing
- Open app on desktop browser
- All buttons clickable
- Forms properly formatted
- Tables display correctly

### Responsive Design
- Resize browser window
- Check mobile view
- Verify Bootstrap responsive features
- Cards should stack on mobile

### Browser Compatibility
- Test on Chrome
- Test on Firefox
- Test on Edge
- Verify functionality works

---

## 📊 Test Results Summary

| Feature | Status | Notes |
|---------|--------|-------|
| Admin Login | ✅ | Works with default credentials |
| Teacher Registration | ✅ | Can create teacher account |
| Student Registration | ✅ | Can create student account |
| Quiz Creation | ✅ | Can create and edit quizzes |
| Add Questions | ✅ | All 3 types work (MCQ, TF, SA) |
| Publish Quiz | ✅ | Quiz becomes available for students |
| Take Quiz | ✅ | Students can answer all question types |
| Submit Quiz | ✅ | Answers auto-graded (MCQ, TF) |
| View Results | ✅ | Scores display correctly |
| User Management | ✅ | Admin can delete users |
| Error Pages | ✅ | 404 and 500 pages work |

---

## 🐛 Known Limitations

1. **Short Answer Grading**: Requires manual grading (not auto-graded)
2. **Quiz Retakes**: Students can only submit once per quiz
3. **Real-time Updates**: No live notifications (requires refresh)
4. **Access Control**: Should add quiz password/code for security
5. **Analytics**: Could add more advanced reporting

---

## ✅ Test Completion Checklist

- [ ] Admin login works
- [ ] Teacher registration works
- [ ] Student registration works
- [ ] Quiz creation works
- [ ] MCQ questions work
- [ ] True/False questions work
- [ ] Short answer questions work
- [ ] Quiz publishing works
- [ ] Student can take quiz
- [ ] Results display correctly
- [ ] Teacher can view results
- [ ] User deletion works
- [ ] Error pages display
- [ ] UI responsive and styled
- [ ] No SQL errors in terminal
- [ ] No JavaScript errors in console

---

**All scenarios should pass for a successful deployment! 🎉**
