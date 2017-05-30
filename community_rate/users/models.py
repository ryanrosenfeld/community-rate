from django.db import models
from general.models import SiteUser


class Follower(models.Model):
	date_followed = models.DateTimeField(auto_now_add=True, editable=False)
	follower = models.ForeignKey(SiteUser, related_name="follower_set")
	following = models.ForeignKey(SiteUser, related_name="following_set")

