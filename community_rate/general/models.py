from django.db import models
from django.contrib.auth.models import AbstractUser


class SiteUser(AbstractUser):
    fb_id = models.CharField(max_length=100, null=True)

    country = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    postal = models.CharField(max_length=6, null=True)
    bio = models.CharField(max_length=500, null=True)

class Notification(models.Model):
    message = models.CharField(max_length=300)
    is_read = models.BooleanField(default=False)

    class_choices = (
        ('Follower', 'Follower'),
        )
    notification_class = models.CharField(max_length=20, choices=class_choices)

    user = models.ForeignKey(SiteUser)