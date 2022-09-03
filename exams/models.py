from django.db import models
from django.utils import timezone

from hta_platform.models import University, Subject


class Exam(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    exam_date = models.DateTimeField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def is_upcoming(self):
        if self.exam_date > timezone.now():
            return True
        else:
            return False
