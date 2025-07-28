from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from exam import views

urlpatterns = [
    path('', lambda request: redirect('landing_page')),  # Redirect root URL to landing page
    path('landing_page/', views.landing_page, name='landing_page'),
    path('signup/', views.student_signup, name='student_signup'),
    path('login/', views.student_login, name='student_login'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('admin/', views.admin_login, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/', views.admin_signup, name='admin_signup'),

]
