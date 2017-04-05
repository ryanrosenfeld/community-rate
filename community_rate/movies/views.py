from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ReviewForm
from .models import Review
from .services import *


def movie_page(request, id):
    try:
        r = Review.objects.get(movie_id=id, user_id=request.user.id)
    except Review.DoesNotExist:
        r = None
    movie = get_movie_by_id(id)
    # img = get_poster_img(movie, 'w92')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            t = request.POST.get('thoughts', None)
            if r is None:
                review = Review(rating=request.POST['rating'], reaction=request.POST['reaction'], thoughts=t,
                                movie_id=id, user_id=request.user.id)
                review.save()
            else:
                r.rating = request.POST['rating']
                r.reaction = request.POST['reaction']
                r.thoughts = request.POST['thoughts']
                r.save()
            return render(request, 'movies/movie.html', {'movie': movie, 'form': form, 'review': r})
    if r is None:
        form = ReviewForm()
    else:
        form = ReviewForm({
            'rating': r.rating,
            'reaction': r.reaction,
            'thoughts': r.thoughts,
        })
    return render(request, 'movies/movie.html', {'movie': movie, 'form': form, 'review': r})


def search(request):
    if request.method == 'GET':
        s = request.GET.get('search', None)
        if s is not None:
            movies = search_movies(s)
            return render(request, 'movies/search-results.html', {'movies': movies})
    else:
        return HttpResponseRedirect('/')