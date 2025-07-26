from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect 
from exam import views

urlpatterns = [
    path('', lambda request: redirect('Student_signup')), 
    path('signup/', views.Student_signup, name='Student_signup'),  
    path('login/', views.Student_login, name='Student_login'),
    path('student/dashboard/', views.student_dashboard, name='Student_dashboard'),
]
