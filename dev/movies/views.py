from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import ReviewForm
from .models import List, ListEntry
from .services import *
from .functions import *


@login_required
def movie_page(request, id):
    try:
        r = Review.objects.get(movie_id=id, creator=request.user)
    except Review.DoesNotExist:
        r = None
    movie = get_movie_by_id(id, False)

    # Get following user reviews, calc average review
    following_users = get_following_user_reviews(request.user, id)
    av_review = calc_average_review(following_users)
    av_rating = av_review[0]
    most_common_react = av_review[1]

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
            return render(request, 'movies/movie.html', {'movie': movie, 'form': form, 'review': r,
                                                         'following_users': following_users, 'av_rating': av_rating,
                                                         'common_react': most_common_react, 'page': 'movies'})
    if r is None:
        form = ReviewForm()
    else:
        form = ReviewForm({
            'rating': r.rating,
            'reaction': r.reaction,
            'thoughts': r.thoughts,
        })
    return render(request, 'movies/movie.html', {'movie': movie, 'form': form, 'review': r,
                                                 'following_users': following_users, 'av_rating': av_rating,
                                                 'common_react': most_common_react, 'page': 'movies'})


@login_required
def movie_db(request):
    query = None
    if request.method == 'GET':
        query = request.GET.get('search', None)
    return render(request, 'movie-db.html', {'page': 'movie_db', 'query': query})


@login_required
def top_movies(request):
    # Get following users
    following = [f.following for f in request.user.follower_set.all()]

    # Top movies: Tuple (movie, av rating, most common react, number of reviews)
    top = []

    # Collect all relevant movie information from all friend reviews
    movies = {}
    for user in following:
        reviews = Review.objects.filter(creator=user)
        for review in reviews:
            if review.movie_id not in movies:
                movies[review.movie_id] = {'movie': Movie.objects.get(movie_id=review.movie_id), 'count': 1,
                                           'sum': review.rating, 'reactions': [review.reaction]}
            else:
                current = movies[review.movie_id]
                current['count'] += 1
                current['sum'] += review.rating
                current['reactions'].append(review.reaction)

    # Organize movie information into list of top movies
    for movie_id, movie in movies.items():
        average_rating = "{0:.1f}".format(float(movie['sum']) / movie['count'])
        top.append((movie['movie'], average_rating, most_common(movie['reactions']), movie['count']))

    # Sort top movies by rating
    top = sorted(top, key=lambda x: (float(x[1]), x[3]), reverse=True)

    return render(request, 'top-movies.html', {'page': 'top_movies', 'top_movies': top})


@login_required
def lists(request):
    # Get all friend's lists
    following = request.user.follower_set.all()
    friend_lists = []
    for f in following:
        user = f.following
        ls = List.objects.filter(creator=user, public=True)
        for l in ls:
            num_movies = len(ListEntry.objects.filter(list=l))
            likes = len(l.likers.all())
            friend_lists.append((l, num_movies, likes))
    friend_lists = sorted(friend_lists, key=lambda x: (x[2], x[0].date_updated), reverse=True)


    # Get user's lists
    ls = List.objects.filter(creator=request.user)
    my_lists = []
    for l in ls:
        num_movies = len(ListEntry.objects.filter(list=l))
        likes = len(l.likers.all())
        my_lists.append((l, num_movies, likes))
    my_lists = sorted(my_lists, key=lambda x: x[0].date_updated, reverse=True)


    # Get lists user can edit
    ls = request.user.editor_set.all()
    shared_lists = []
    for l in ls:
        num_movies = len(ListEntry.objects.filter(list=l))
        likes = len(l.likers.all())
        shared_lists.append((l, num_movies, likes))
    shared_lists = sorted(shared_lists, key=lambda x: x[0].date_updated, reverse=True)

    return render(request, 'movies/lists.html', {'friend_lists': friend_lists,
                                                 'my_lists': my_lists,
                                                 'shared_lists': shared_lists,
                                                 'page': 'lists'})


@login_required
def list_page(request, list_id):
    # Get list
    l = List.objects.filter(id=list_id)
    if len(l) == 0:
        return HttpResponseRedirect('/profile/')
    l = l[0]
    print(l.id)

    # Get editors
    editors = l.editors.all()
    print(editors)

    # Check if list creator
    owner = l.creator == request.user

    # Check if user possesses editor rights
    editor = request.user in editors

    # Check if list liked
    liked = False
    if not owner:
        if len(List.objects.filter(id=list_id, likers=request.user)) > 0:
            liked = True

    # Collect entries
    entries = ListEntry.objects.filter(list=l)
    movies = []
    for e in entries:
        # Get movie info
        movie_id = e.movie_id
        movie = get_movie_by_id(movie_id, True)
        if movie.poster_path is not None:
            movie.img_path = 'http://image.tmdb.org/t/p/w92' + movie.poster_path
        else:
            movie.img_path = "{% static 'general/img/no_poster.jpg'}"

        # Get my review info
        try:
            my_review = Review.objects.get(movie_id=movie_id, creator=request.user)
        except Review.DoesNotExist:
            my_review = None

        # Get average review info
        following_users = get_following_user_reviews(request.user, movie_id)
        if my_review is not None:
            following_users.append((request.user, my_review))
        average_review = calc_average_review(following_users)

        movies.append((movie, my_review, average_review))

    # Get following set
    following = [user.following for user in request.user.follower_set.all() if user.following not in editors]

    return render(request, 'list.html', {'list': l, 'movies': movies, 'owner': owner, 'liked': liked, 'page': 'lists',
                                         'following': following, 'editors': editors, 'editor': editor})


@login_required
def new_list(request):
    l = List(creator=request.user)
    l.save()
    return HttpResponseRedirect('/list/' + str(l.id) + '/')


@login_required
def delete_list(request, list_id):
    l = List.objects.filter(id=int(list_id))
    if len(l) == 0:
        return HttpResponseRedirect('/lists/')
    l = l[0]
    l.delete()
    return HttpResponseRedirect('/lists/')
