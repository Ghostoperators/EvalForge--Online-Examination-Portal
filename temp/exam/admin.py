from django.contrib import admin
from .models import Admin, Subject, Student, Question, ExamResult

admin.site.register(Admin)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Question)
admin.site.register(ExamResult)
