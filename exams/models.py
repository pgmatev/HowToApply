from django.db import models
from django.utils import timezone

from django.core.validators import MinValueValidator, MaxValueValidator

from hta_platform.models import University, Student, Subject


class Exam(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    exam_date = models.DateTimeField()
    deadline = models.DateTimeField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    @property
    def is_upcoming(self):
        if self.exam_date > timezone.now():
            return True
        else:
            return False

    @property
    def past_deadline(self):
        if self.deadline < timezone.now():
            return True
        else:
            return False


class StudentExam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey("exams.Exam", on_delete=models.DO_NOTHING)
    mark = models.DecimalField(null=True, blank=True, max_digits=3, decimal_places=2,
                               validators=[MinValueValidator(2.00), MaxValueValidator(6.00)])

    class Meta:
        unique_together = ('student', 'exam')

    # @classmethod
    # def create(cls, student, exam):
    #     student_exam = cls(student=student, exam=exam)
    #
    #     return student_exam