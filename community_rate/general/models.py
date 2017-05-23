from django.db import models
from django.contrib.auth.models import AbstractUser


class SiteUser(AbstractUser):
<<<<<<< HEAD
    fb_id = models.CharField(max_length=100, null=True)
=======
    fb_id = models.CharField(unique=True, max_length=100, blank=True)
    fav_quote = models.TextField(blank=True)
    about_me = models.TextField(blank=True)
>>>>>>> develop
