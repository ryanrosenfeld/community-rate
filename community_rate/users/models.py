from django.db import models
from general.models import SiteUser

# class Friend(models.Model):
# 	created = models.DateTimeField(auto_now_add=True, editable=False)
# 	creator = models.ForeignKey(SiteUser, related_name="friendship_creator_set")
# 	friend = models.ForeignKey(SiteUser, related_name="friend_set")

class Follower(models.Model):
	date_followed = models.DateTimeField(auto_now_add=True, editable=False)
	follower = models.ForeignKey(SiteUser, related_name="follower_set")
	following = models.ForeignKey(SiteUser, related_name="following_set")