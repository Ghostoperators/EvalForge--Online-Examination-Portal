from django.urls import path
from django.shortcuts import redirect
from exam import views

urlpatterns = [
    path('', lambda request: redirect('landing_page')),

    path('landing_page/', views.landing_page, name='landing_page'),

    # Student
    path('signup/', views.student_signup, name='student_signup'),
    path('login/', views.student_login, name='student_login'),
    path('student/', views.student_dashboard, name='student_dashboard'),

    # Admin
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_signup/', views.admin_signup, name='admin_signup'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Subject/Question management
    path('admin/add_subject/', views.add_subject, name='add_subject'),
    path('subject/<int:subject_id>/add_question/', views.add_question, name='add_question'),
    path('subject/<int:subject_id>/delete/', views.delete_subject, name='delete_subject'),
    path('subject/<int:subject_id>/delete_question/', views.delete_question, name='delete_question'),
    path('subject/<int:subject_id>/questions/', views.view_questions, name='view_questions'),
    path('start_exam/<int:subject_id>/', views.start_exam, name='start_exam'),

    # Logout
    path('logout/', views.logout_view, name='logout'),
]
