from django.shortcuts import render, redirect
from .models import Student, Subject, ExamResult, Admin
from django.contrib.auth.hashers import make_password, check_password


def landing_page(request):
    return render(request, 'Landing_page.html')


def student_signup(request):
    if request.method == 'POST':
        loginid = request.POST.get('loginid')
        raw_password = request.POST.get('password')
        password = make_password(raw_password)  # hash password before saving
        enroll = request.POST.get('enroll')
        email = request.POST.get('email')
        contact = request.POST.get('contact')

        # Check if loginid already exists
        if Student.objects.filter(loginid=loginid).exists():
            return render(request, 'Student_signup.html', {'error': 'Login ID already exists'})

        # Optionally you can also check uniqueness for enroll/email here

        student = Student.objects.create(
            loginid=loginid,
            password=password,
            enroll=enroll,
            email=email,
            contact=contact
        )
        request.session['student_id'] = student.id
        return redirect('student_dashboard')  # Use lowercase name

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
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return redirect('student_login')  # In case session is invalid or deleted

    subjects = Subject.objects.all()
    results = ExamResult.objects.filter(student_id=student_id)

    context = {
        'student': student,
        'subjects': subjects,
        'results': results,
    }
    return render(request, 'Student_dashboard.html', context)


def admin_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Replace with your admin authentication logic:
        if username == 'admin' and password == 'admin123':  # example static check
            request.session['admin_logged_in'] = True
            return redirect('admin_dashboard')  # Define this URL and view
        else:
            error = 'Invalid username or password'

    return render(request, 'Admin_login.html', {'error': error})

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
            # You can log them in or redirect as needed
            request.session['admin_id'] = admin.id
            return redirect('admin_dashboard')  # Update this URL to match your project

    return render(request, 'Admin_signup.html', {'error': error})


def logout_view(request):
    # Clear the session when user logs out (can be for both admin/student)
    request.session.flush()
    return redirect('landing_page')
