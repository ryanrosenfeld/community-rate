from django.db import models
from django.contrib.auth.models import AbstractUser


class SiteUser(AbstractUser):
    fb_id = models.CharField(max_length=100, blank=True)
    fav_quote = models.TextField(blank=True)
    about_me = models.TextField(blank=True)
    has_pic = models.BooleanField(default=False)


class Notification(models.Model):
    message = models.CharField(max_length=300)
    is_read = models.BooleanField(default=False)

    class_choices = (
        ('Follower', 'Follower'),
        )
    notification_class = models.CharField(max_length=20, choices=class_choices)

    user = models.ForeignKey(SiteUser)
