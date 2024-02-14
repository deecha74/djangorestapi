from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Posts(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]


class Votes(models.Model):
    posts = models.ForeignKey(Posts, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
