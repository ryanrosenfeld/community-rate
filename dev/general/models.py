from django.db import models
from django.contrib.auth.models import AbstractUser


class SiteUser(AbstractUser):
    fb_id = models.CharField(max_length=100, blank=True)
    fav_quote = models.TextField(blank=True)
    about_me = models.TextField(blank=True)
    timezone = models.CharField(max_length=100, default="US/Eastern")
    profile_pic = models.TextField(blank=True)
    reset_key = models.TextField(default='1')
    show_welcome = models.BooleanField(default=True)


class Notification(models.Model):
    message = models.CharField(max_length=300)
    url = models.CharField(max_length=200, blank=True)
    is_read = models.BooleanField(default=False)
    user = models.ForeignKey(SiteUser)
