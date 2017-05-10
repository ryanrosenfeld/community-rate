from django.db import models
from django.contrib.auth.models import AbstractUser


class SiteUser(AbstractUser):
    fb_id = models.CharField(unique=True, max_length=100)
    fav_quote = models.TextField(blank=True)
    about_me = models.TextField(blank=True)
