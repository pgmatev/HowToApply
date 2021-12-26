from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.functional import empty

class University(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    website = models.URLField()

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(University, on_delete=models.CASCADE)




