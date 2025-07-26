from django.shortcuts import render, redirect
from . models import Student

def Student_signup(request):
    if request.method == 'POST':
        loginid = request.POST.get('loginid')
        password = request.POST.get('password')
        enroll = request.POST.get('enroll')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        if Student.objects.filter(loginid=loginid).exists():
            return render(request, 'login/Student_signup.html', {'error': 'Login ID already exists'})
        Student.objects.create(
            loginid=loginid,
            password=password,
            enroll=enroll,
            email=email,
            contact=contact
        )
        return redirect('Student_login')
    return render(request, 'login/Student_signup.html')


def Student_login(request):
    error = None
    if request.method == 'POST':
        loginid = request.POST.get('loginid')
        password = request.POST.get('password')
        try:
            student = Student.objects.get(loginid=loginid, password=password)
            request.session['student_id'] = student.id  
            return redirect('student_dashboard')
        except Student.DoesNotExist:
            error = 'Invalid login ID or password'
    return render(request, 'login/Student_Login.html', {'error': error})

def student_dashboard(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login/student_login') 

    student = Student.objects.get(id=student_id)
    return render(request, 'student/student_dashboard.html', {'student': student})
