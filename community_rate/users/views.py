from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from movies.models import Review
from movies.services import get_movie_by_id
from general.models import SiteUser
from .models import *

def profile(request):
    reviews = Review.objects.filter(user_id=request.user.id)
    for r in reviews:
        r.movie = get_movie_by_id(r.movie_id)
    favorites = sorted(reviews, key=lambda x: x.rating, reverse=True)
    recents = sorted(reviews, key=lambda x: x.date_added, reverse=True)
    return render(request, 'users/profile.html', {'favorites': favorites, 'recents': recents, 'page': 'profile'})

def view_users(request):
	all_users = SiteUser.objects.all()
	return render(request, 'users/all.html', {'users': all_users})

def main_view(request, response=None):
	"""Main view for users page"""

	users = []

	# Find this user's followers, following
	following = request.user.follower_set.all()

	followers = request.user.following_set.all()

	# Retrieve all users
	all_users = SiteUser.objects.all()

	# Append their follower count and
	# whether or not they are already following that person
	for user in all_users:
		# Find follower count
		followers_count = len(user.following_set.all())

		# Determine if this user is already following them OR
		# request user is actually this user
		query = following.filter(following=user)
		already_following = (len(query) > 0) | (user == request.user)

		users.append((user,followers_count, already_following))

	# Sort by follower count (highest first)
	users = sorted(users, key=lambda x: x[1], reverse=True)

	return render(request, 'users/main.html', {'followers': len(followers), 
		'following': len(following), 
		'users': users,
		'response': response})

def follow(request, username):
	"""Creates follow connection between requester and person they wish to follow"""

	# Retrieve the SiteUser account of the person they wish to follow
	try:
		following_user = SiteUser.objects.get(username=username)

	except ObjectDoesNotExist:
		response = "User \"{0}\" does not exist".format(username)
		return main_view(request, response)

	# Determine if this user is already following them
	query = request.user.follower_set.filter(following=following_user)
	already_following = len(query) > 0

	if already_following:
		response = "You are already following {0}!".format(username)
		return main_view(request, response)

	# Person exists and this user is not already following them
	f = Follower.objects.create(follower=request.user, following=following_user)
	f.save()

	response = "You are now following {0}".format(username)
	return main_view(request, response)