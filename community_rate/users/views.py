from django.shortcuts import render
from movies.models import Review
from general.models import SiteUser
from movies.services import get_movie_by_id


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

def main_view(request):
	users = []
	all_users = SiteUser.objects.all()

	for user in all_users:
		followers_count = len(user.follower_set.all())
		users.append((user,followers_count))
	print(request.user.username)
	print(len(all_users))
	followers = request.user.follower_set.all()
	print(followers)
	following = request.user.following_set.all()
	return render(request, 'users/main.html', {'followers': len(followers), 
		'following': len(following), 
		'users': users})