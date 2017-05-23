from django.db import models
from general.models import SiteUser


class Movie(models.Model):
    movie_id = models.IntegerField()
    title = models.CharField(max_length=100)
    poster_path = models.TextField()


class Review(models.Model):
    rating = models.IntegerField()
    reaction = models.CharField(
        max_length=100
    )
    movie_id = models.IntegerField()
    user_id = models.IntegerField()
    thoughts = models.CharField(
        max_length=10000,
    )
    date_added = models.DateTimeField(auto_now=True)


class List(models.Model):
    creator = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    date_updated = models.DateTimeField(auto_now=True)


class ListEntry(models.Model):
    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    list = models.ForeignKey(List)
    movie_id = models.IntegerField()
