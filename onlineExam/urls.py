from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect 
from exam import views
urlpatterns = [
    path('', lambda request: redirect('student_login')),  
    path('login/', views.student_login, name='student_login'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
]

