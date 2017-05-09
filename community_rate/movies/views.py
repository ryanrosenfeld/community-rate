from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from .forms import ReviewForm
from .models import Review
from .services import *


def movie_page(request, id):
    try:
        r = Review.objects.get(movie_id=id, user_id=request.user.id)
    except Review.DoesNotExist:
        r = None
    movie = get_movie_by_id(id)
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


def movie_db(request):
    query = None
    if request.method == 'GET':
        query = request.GET.get('search', None)
    print(query)
    return render(request, 'movie-db.html', {'page': 'movies', 'query': query})


def search(request):
    if request.method == 'GET':
        query = request.GET.get('search', None)
        return render(request, 'movies/search-results.html', {'query': query, 'page': 'movies'})
    return HttpResponseRedirect('/')


def filter_movies(request):
    if request.method == 'GET':
        s = request.GET.get('query', None)
        if s is not None:
            movies = search_movies(s)
            return JsonResponse(movies)
    return JsonResponse({})


def get_movie_rating(request):
    m_id = request.GET.get('movie', None)

    if m_id is not None:
        reviews = Review.objects.filter(movie_id=m_id)
        rating = {
            'average_rating': 0
        }
        if len(reviews) > 0:
            rating = {
                'average_rating': sum(r.rating for r in reviews) / len(reviews)
            }
    return JsonResponse(rating)


# def search_movies(request):
#     if request.method == 'GET':
#         s = request.GET.get('query', None)
#         if s is not None:
#             movies = search_movies(s)
#             return JsonResponse(movies)
#     return JsonResponse({})
