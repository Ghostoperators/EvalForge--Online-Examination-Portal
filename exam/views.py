from django.shortcuts import render, redirect
from . models import Student

def student_login(request):
    error = None
    if request.method == 'POST':
        loginid = request.POST.get('loginid')
        password = request.POST.get('password')
        try:
            student = Student.objects.get(loginid=loginid, password=password)
            request.session['student_id'] = student.id  # store in session
            return redirect('student_dashboard')
        except Student.DoesNotExist:
            error = 'Invalid login ID or password'
    return render(request, 'login/Student_Login.html', {'error': error})

def student_dashboard(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login/student_login')  # if not logged in

    student = Student.objects.get(id=student_id)
    return render(request, 'student/student_dashboard.html', {'student': student})
