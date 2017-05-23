from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from .forms import ReviewForm
from .models import Review, List, ListEntry
from .services import *


def movie_page(request, id):
    try:
        r = Review.objects.get(movie_id=id, user_id=request.user.id)
    except Review.DoesNotExist:
        r = None
    movie = get_movie_by_id(id, False)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            t = request.POST.get('thoughts', None)
            if r is None:
                review = Review(rating=request.POST['rating'], reaction=request.POST['reaction'], thoughts=t,
                                movie_id=id, user_id=request.user.id)
                review.save()
                r = review
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


def new_list(request):
    l = List(creator=request.user)
    l.save()
    return HttpResponseRedirect('/edit-list/' + str(l.id) + '/')


def edit_list(request, list_id):
    l = List.objects.filter(id=list_id)
    if len(l) == 0:
        return HttpResponseRedirect('/profile/')
    entries = ListEntry.objects.filter(list=l)
    movies = []
    for e in entries:
        movie_id = e.movie_id
        movie = get_movie_by_id(movie_id, True)
        if movie.poster_path is not None:
            movie.img_path = 'http://image.tmdb.org/t/p/w92' + movie.poster_path
        else:
            movie.img_path = "{% static 'general/img/no_poster.jpg'}"
        movies.append(movie)
    return render(request, 'new-list.html', {'list_id': list_id, 'movies': movies})


# AJAX views
def filter_movies(request):
    if request.method == 'GET':
        s = request.GET.get('query', None)
        if s is not None:
            movies = search_movies(s)
            return JsonResponse(movies)
    return JsonResponse({})


def get_movie_info(request):
    movie_id = request.GET.get('id', None)
    if movie_id is not None:
        movie = get_movie_by_id(movie_id, False)
        return JsonResponse(movie)
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
                'average_rating': "{0:.1f}".format(sum(r.rating for r in reviews) / len(reviews))
            }
    return JsonResponse(rating)


def add_list_entry(request):
    list_id = request.GET.get('list_id', None)
    movie_id = request.GET.get('movie_id', None)

    l = List.objects.filter(id=list_id)[0]
    le = ListEntry(list=l, movie_id=movie_id)
    le.save()
    return JsonResponse({})
