from django.db import models

class Subject(models.Model):
    subname = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.subname

class Student(models.Model):
    enroll = models.CharField(max_length=20)
    loginid = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # store hashed password
    email = models.EmailField()
    contact = models.CharField(max_length=15)

    class Meta:
        db_table = "student"

    def __str__(self):
        return self.loginid

class Question(models.Model):
    question = models.CharField(max_length=255)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    correctanswer = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.question

class ExamResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    totalmarks = models.IntegerField()
    totalquestion = models.IntegerField()

class Admin(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Hashed password
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username
