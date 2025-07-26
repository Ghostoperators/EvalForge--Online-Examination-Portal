from django.db import models

class Admin(models.Model):
    loginid = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

class Subject(models.Model):
    subname = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Student(models.Model):
    enroll = models.CharField(max_length=20)
    loginid = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    class Meta:
        db_table = "student"
class Question(models.Model):
    question = models.CharField(max_length=255)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    correctanswer = models.CharField(max_length=100)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    def __str__(self):
        return self.question

class ExamResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    totalmarks = models.IntegerField()
    totalquestion = models.IntegerField()
