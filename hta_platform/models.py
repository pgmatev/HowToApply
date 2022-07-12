from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Subject(models.Model):
    subject = models.CharField(max_length=100)


class University(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    website = models.URLField()


class Exam(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    exam_date = models.DateTimeField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True)
    obligatory_mark = models.DecimalField(null=True, max_digits=3, decimal_places=2,
                                           validators=[MinValueValidator(2.00), MaxValueValidator(6.00)])
    exams = models.ManyToManyField(Exam, through='StudentExam')


class StudentExam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.DO_NOTHING)
    mark = models.DecimalField(null=True, max_digits=3, decimal_places=2,
                                validators=[MinValueValidator(2.00), MaxValueValidator(6.00)])


class Program(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    obligatory_coef = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(3.0)]
    )
    exams = models.ManyToManyField(Exam, through='ProgramExam')


class ProgramExam(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.DO_NOTHING)
    coef = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(3.0)]
    )


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(null=False, unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(University, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify_unique(self.title, Post)
        super(Post, self).save(*args, **kwargs)


def slugify_unique(value, model, slugfield="slug"):  # increments slugs of posts that share a title
    suffix = 0
    potential = base = slugify(value)
    while True:
        if suffix:
            potential = "-".join([base, str(suffix)])
        if not model.objects.filter(**{slugfield: potential}).count():
            return potential
        suffix += 1
