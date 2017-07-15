from django.db import models
from general.models import SiteUser


class Movie(models.Model):
    movie_id = models.IntegerField()
    title = models.CharField(max_length=100)
    poster_path = models.TextField()
    release_year = models.IntegerField()


class Review(models.Model):
    creator = models.ForeignKey(SiteUser)
    rating = models.IntegerField()
    reaction = models.CharField(
        max_length=100,
    )
    movie_id = models.IntegerField()
    thoughts = models.CharField(
        max_length=10000,
        blank=True
    )
    date_added = models.DateTimeField(auto_now=True)


class List(models.Model):
    creator = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='Untitled')
    date_updated = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=True)
    editors = models.ManyToManyField(SiteUser, related_name="editor_set")
    likers = models.ManyToManyField(SiteUser, related_name="liker_set")


class ListEntry(models.Model):
    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    list = models.ForeignKey(List)
    movie_id = models.IntegerField()


class Comment(models.Model):
    author = models.ForeignKey(SiteUser)
    review = models.ForeignKey(Review)
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now=True)
