from django.shortcuts import render, redirect
from .models import Student, Subject, ExamResult

def Student_signup(request):
    if request.method == 'POST':
        loginid = request.POST.get('loginid')
        password = request.POST.get('password')
        enroll = request.POST.get('enroll')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        
        if Student.objects.filter(loginid=loginid).exists():
            return render(request, 'login/Student_signup.html', {'error': 'Login ID already exists'})
        
        student = Student.objects.create(
            loginid=loginid,
            password=password,
            enroll=enroll,
            email=email,
            contact=contact
        )
        request.session['student_id'] = student.id
        return redirect('Student_dashboard')  # ✅ Redirect directly to dashboard
    
    return render(request, 'login/Student_signup.html')


def Student_login(request):
    error = None
    if request.method == 'POST':
        loginid = request.POST.get('loginid')
        password = request.POST.get('password')
        try:
            student = Student.objects.get(loginid=loginid, password=password)
            request.session['student_id'] = student.id
            return redirect('Student_dashboard')  # ✅ Correct URL name
        except Student.DoesNotExist:
            error = 'Invalid login ID or password'
    
    return render(request, 'login/Student_Login.html', {'error': error})


from django.shortcuts import render, redirect
from .models import Student, Subject, ExamResult

def student_dashboard(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('Student_login')
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return redirect('Student_login')  # In case session is invalid
    subjects = Subject.objects.all()
    results = ExamResult.objects.filter(student_id=student_id)
    context = {
        'student': student,
        'subjects': subjects,
        'results': results,
    }

    return render(request, 'student/Student_dashboard.html', context)
