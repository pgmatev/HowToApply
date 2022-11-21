from django.db import models
# from django.apps import apps
from django.utils import timezone

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Exam = apps.get_model('exams', 'Exam')


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


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null = True)
    bio = models.TextField(null=True, blank=True)
    obligatory_mark = models.DecimalField(null=True, max_digits=3, decimal_places=2,
                                          validators=[MinValueValidator(2.00), MaxValueValidator(6.00)])
    exams = models.ManyToManyField("exams.Exam", through='exams.StudentExam')

    def __str__(self):
        return self.user.username

    @property
    def calculate_age(self):
        diff = timezone.now().date() - self.birthday
        return int(diff.days/365)
