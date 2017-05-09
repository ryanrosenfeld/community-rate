from django.db import models
from django.contrib.auth.models import AbstractUser


class SiteUser(AbstractUser):
    fb_id = models.CharField(max_length=100, null=True)
