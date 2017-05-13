from django.db import models
from general.models import SiteUser

class Review(models.Model):
    creator = models.ForeignKey(SiteUser)
    rating = models.IntegerField()
    reaction = models.CharField(
        max_length=100
    )
    movie_id = models.IntegerField()
    thoughts = models.CharField(
        max_length=10000,
    )
    date_added = models.DateTimeField(auto_now=True)
