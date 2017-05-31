from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from .forms import ReviewForm
from .models import Review, List, ListEntry
from .services import *


def movie_page(request, id):
    try:
        r = Review.objects.get(movie_id=id, creator=request.user)
    except Review.DoesNotExist:
        r = None
    movie = get_movie_by_id(id, False)

    # Get following user reviews
    following = request.user.follower_set.all()
    following_users = []
    for follower_obj in following:
        user = follower_obj.following
        try:
            rev = Review.objects.get(movie_id=id, creator=user)
        except Review.DoesNotExist:
            rev = None
        if rev is not None:
            following_users.append((follower_obj.following, rev))

    # Calculate average rating
    av_rating = float(sum(r.rating for u, r in following_users)) / len(following_users)
    av_rating = "{0:.1f}".format(av_rating)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            t = request.POST.get('thoughts', None)
            if r is None:
                review = Review(rating=request.POST['rating'], reaction=request.POST['reaction'], thoughts=t,
                                movie_id=id, creator=request.user)
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
    return render(request, 'movies/movie.html', {'movie': movie, 'form': form, 'review': r,
                                                 'following_users': following_users, 'av_rating': av_rating})


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
    l = l[0]
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
    return render(request, 'edit-list.html', {'list': l, 'movies': movies})


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


def update_list_name(request):
    list_id = request.GET.get('list_id', None)
    name = request.GET.get('name', None)

    l = List.objects.filter(id=list_id)[0]
    l.name = name
    l.save()
    return JsonResponse({})


def remove_list_item(request):
    list_id = request.GET.get('list_id', None)
    movie_id = request.GET.get('movie_id', None)

    l = List.objects.filter(id=list_id)[0]
    le = ListEntry.objects.filter(list=l, movie_id=movie_id)[0]
    le.delete()
    return JsonResponse({})
