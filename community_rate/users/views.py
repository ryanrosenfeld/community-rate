from django.shortcuts import render
from movies.models import Review
from movies.services import get_movie_by_id


def profile(request):
    reviews = Review.objects.filter(user_id=request.user.id)
    for r in reviews:
        r.movie = get_movie_by_id(r.movie_id)
    favorites = sorted(reviews, key=lambda x: x.rating, reverse=True)
    recents = sorted(reviews, key=lambda x: x.date_added, reverse=True)
    return render(request, 'users/profile.html', {'favorites': favorites, 'recents': recents})
