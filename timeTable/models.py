from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Semester(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Division(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Classroom(models.Model):
    name = models.CharField(max_length=100,null=True,default=None)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Faculty(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Day(models.Model):
    day = models.CharField(max_length=250)

    def __str__(self):
        return self.day

class AssignSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.CharField(max_length=100)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

class TimeTable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True) 
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE,null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.ForeignKey,null=True)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
