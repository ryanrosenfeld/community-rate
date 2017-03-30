from django.db import models
from django.contrib.auth.models import AbstractUser


class SiteUser(AbstractUser):
    fb_id = models.CharField(unique=True, max_length=100)


class Review(models.Model):
    rating = models.IntegerField()
    reaction = models.CharField(
        max_length=100
    )
    movie_id = models.IntegerField()
    thoughts = models.CharField(
        max_length=10000,
    )
