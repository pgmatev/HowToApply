from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator

from hta_platform.models import University
from exams.models import Exam


class Program(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    obligatory_coef = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(3.0)]
    )
    exams = models.ManyToManyField(Exam, through='ProgramExam')

    def __str__(self):
        return self.name


class ProgramExam(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    coef = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(3.0)]
    )

    class Meta:
        unique_together = ('program', 'exam')
