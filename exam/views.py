from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Subject, ExamResult, Admin, Question
from django.contrib.auth.hashers import make_password, check_password

def landing_page(request):
    return render(request, 'Landing_page.html')

# Student Views

def student_signup(request):
    if request.method == 'POST':
        loginid = request.POST.get('loginid')
        raw_password = request.POST.get('password')
        password = make_password(raw_password)
        enroll = request.POST.get('enroll')
        email = request.POST.get('email')
        contact = request.POST.get('contact')

        if Student.objects.filter(loginid=loginid).exists():
            return render(request, 'Student_signup.html', {'error': 'Login ID already exists'})
        Student.objects.create(
            loginid=loginid,
            password=password,
            enroll=enroll,
            email=email,
            contact=contact
        )
        student = Student.objects.get(loginid=loginid)
        request.session['student_id'] = student.id
        return redirect('student_dashboard')
    return render(request, 'Student_signup.html')

def student_login(request):
    error = None
    if request.method == 'POST':
        loginid = request.POST.get('loginid')
        raw_password = request.POST.get('password')
        try:
            student = Student.objects.get(loginid=loginid)
            if check_password(raw_password, student.password):
                request.session['student_id'] = student.id
                return redirect('student_dashboard')
            else:
                error = 'Invalid login ID or password'
        except Student.DoesNotExist:
            error = 'Invalid login ID or password'
    return render(request, 'Student_Login.html', {'error': error})

def student_dashboard(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('student_login')
    student = get_object_or_404(Student, id=student_id)
    subjects = Subject.objects.all()
    results = ExamResult.objects.filter(student_id=student_id)
    context = {
        'student': student,
        'subjects': subjects,
        'results': results,
    }
    return render(request, 'Student_dashboard.html', context)

# Admin Views

def admin_signup(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        raw_password = request.POST.get('password')
        password = make_password(raw_password)
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        if Admin.objects.filter(username=username).exists():
            error = 'Username already exists'
        elif Admin.objects.filter(email=email).exists():
            error = 'Email already registered'
        else:
            admin = Admin.objects.create(
                username=username,
                password=password,
                email=email,
                contact=contact
            )
            request.session['admin_id'] = admin.id
            request.session['admin_logged_in'] = True
            return redirect('admin_dashboard')
    return render(request, 'Admin_signup.html', {'error': error})

def admin_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        raw_password = request.POST.get('password')
        try:
            admin = Admin.objects.get(username=username)
            if check_password(raw_password, admin.password):
                request.session['admin_id'] = admin.id
                request.session['admin_logged_in'] = True
                return redirect('admin_dashboard')
            else:
                error = 'Invalid username or password'
        except Admin.DoesNotExist:
            error = 'Invalid username or password'
    return render(request, 'Admin_login.html', {'error': error})

def admin_dashboard(request):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    admin_id = request.session.get('admin_id')
    admin = get_object_or_404(Admin, id=admin_id)
    subjects = Subject.objects.all().order_by('subname')
    results = ExamResult.objects.select_related('student', 'subject').all()
    context = {
        'admin': admin,
        'subjects': subjects,
        'results': results,
    }
    return render(request, 'Admin_dashboard.html', context)

# Subject Management

def add_subject(request):
    error = None
    if request.method == 'POST':
        subname = request.POST.get('subname', '').strip()
        if not subname:
            error = "Subject name cannot be empty."
        elif Subject.objects.filter(subname__iexact=subname).exists():
            error = "Subject with this name already exists."
        else:
            Subject.objects.create(subname=subname)
            return redirect('admin_dashboard')
    return render(request, 'Add_subject.html', {'error': error})

# Question Management

def add_question(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    error = None
    if request.method == 'POST':
        question_text = request.POST.get('question', '').strip()
        option1 = request.POST.get('option1', '').strip()
        option2 = request.POST.get('option2', '').strip()
        option3 = request.POST.get('option3', '').strip()
        option4 = request.POST.get('option4', '').strip()
        correct_answer = request.POST.get('correctanswer', '').strip()
        if not all([question_text, option1, option2, option3, option4, correct_answer]):
            error = "Please fill all fields."
        elif correct_answer not in [option1, option2, option3, option4]:
            error = "Correct answer must be one of the options."
        if not error:
            Question.objects.create(
                question=question_text,
                option1=option1,
                option2=option2,
                option3=option3,
                option4=option4,
                correctanswer=correct_answer,
                subject=subject
            )
            return redirect('admin_dashboard')
    return render(request, 'Add_question.html', {'subject': subject, 'error': error})

def view_questions(request, subject_id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    subject = get_object_or_404(Subject, id=subject_id)
    questions = subject.question_set.all()
    context = {
        'subject': subject,
        'questions': questions,
    }
    return render(request, 'View_questions.html', context)

def delete_subject(request, subject_id):
    if request.method == 'POST':
        subject = get_object_or_404(Subject, id=subject_id)
        subject.delete()
    return redirect('admin_dashboard')


def delete_question(request, question_id):
    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')
    if request.method == 'POST':
        question = get_object_or_404(Question, id=question_id)
        subject_id = question.subject.id
        question.delete()
        return redirect('view_questions', subject_id=subject_id)
    return redirect('admin_dashboard')



def start_exam(request, subject_id):
    # Ensure student is logged in
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('student_login')
    subject = get_object_or_404(Subject, id=subject_id)
    questions = Question.objects.filter(subject=subject)
    if request.method == 'POST':
        # Process submitted answers
        submitted_answers = {}
        for question in questions:
            ans = request.POST.get(f'question_{question.id}')
            submitted_answers[question.id] = ans
        total_questions = questions.count()
        correct_count = 0

        for question in questions:
            if submitted_answers.get(question.id) == question.correctanswer:
                correct_count += 1
        # Calculate score as number of correct answers
        marks_scored = correct_count

        # Store result in ExamResult table
        student = get_object_or_404(Student, id=student_id)
        ExamResult.objects.create(
            student=student,
            subject=subject,
            totalmarks=marks_scored,
            totalquestion=total_questions
        )
        # You can either show a result page or redirect to dashboard or results
        return render(request, 'exam_result.html', {
            'subject': subject,
            'total_questions': total_questions,
            'marks_scored': marks_scored,
        })
    # GET request: Show test questions
    return render(request, 'start_exam.html', {
        'subject': subject,
        'questions': questions,
    })
def logout_view(request):
    request.session.flush()
    return redirect('landing_page')