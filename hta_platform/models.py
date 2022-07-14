from django.db import models

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Subject(models.Model):
    subject = models.CharField(max_length=100)

    def __str__(self):
        return self.subject


class University(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    website = models.URLField()

    def __str__(self):
        return self.user.username


class Exam(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    exam_date = models.DateTimeField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True)
    obligatory_mark = models.DecimalField(null=True, max_digits=3, decimal_places=2,
                                           validators=[MinValueValidator(2.00), MaxValueValidator(6.00)])
    exams = models.ManyToManyField(Exam, through='StudentExam')

    def __str__(self):
        return self.user.username


class StudentExam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.DO_NOTHING)
    mark = models.DecimalField(null=True, max_digits=3, decimal_places=2,
                                validators=[MinValueValidator(2.00), MaxValueValidator(6.00)])
