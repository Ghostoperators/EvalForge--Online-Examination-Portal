from django.db import models

class Admin(models.Model):
    loginid = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

class Subject(models.Model):
    subname = models.CharField(max_length=100)

class Student(models.Model):
    enroll = models.CharField(max_length=20)
    loginid = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()
    contact = models.CharField(max_length=15)

class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    question_text = models.TextField()
    opt1 = models.CharField(max_length=255)
    opt2 = models.CharField(max_length=255)
    opt3 = models.CharField(max_length=255)
    opt4 = models.CharField(max_length=255)
    cans = models.CharField(max_length=255)

class ExamResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    totalmarks = models.IntegerField()
    totalquestion = models.IntegerField()
