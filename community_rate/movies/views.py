from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from .forms import ReviewForm
from .models import List, ListEntry
from .services import *
from .functions import *


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
                                                         'common_react': most_common_react})
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
                                                 'common_react': most_common_react})


def movie_db(request):
    query = None
    if request.method == 'GET':
        query = request.GET.get('search', None)
    print(query)
    return render(request, 'movie-db.html', {'page': 'movies', 'query': query})


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
    friend_lists = sorted(friend_lists, key=lambda x: x[0].date_updated, reverse=True)


    # Get user's lists
    ls = List.objects.filter(creator=request.user)
    my_lists = []
    for l in ls:
        num_movies = len(ListEntry.objects.filter(list=l))
        likes = len(l.likers.all())
        my_lists.append((l, num_movies, likes))
    my_lists = sorted(my_lists, key=lambda x: (x[2], x[0].date_updated), reverse=True)

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
                                                 'page': "lists"})


def list_page(request, list_id):
    # Get list
    l = List.objects.filter(id=list_id)
    if len(l) == 0:
        return HttpResponseRedirect('/profile/')
    l = l[0]

    # Check if list creator
    owner = l.creator == request.user

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

    return render(request, 'list.html', {'list': l, 'movies': movies, 'owner': owner, 'liked': liked, 'page': 'lists'})


def new_list(request):
    l = List(creator=request.user)
    l.save()
    return HttpResponseRedirect('/list/' + str(l.id) + '/')


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
        movie['release_year'] = movie['release_date'][:4]

        # Get my review info
        try:
            my_review = Review.objects.get(movie_id=movie_id, creator=request.user)
            my_rating = my_review.rating
            my_reaction = my_review.reaction
        except Review.DoesNotExist:
            my_review = None
            my_rating = ''
            my_reaction = ''

        # Get average review info
        following_users = get_following_user_reviews(request.user, movie_id)
        if my_review is not None:
            following_users.append((request.user, my_review))
        average_review = calc_average_review(following_users)

        return JsonResponse({'movie': movie, 'my_rating': my_rating, 'my-reaction': my_reaction,
                             'av_rating': average_review[0], 'av_reaction': average_review[1]})
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


def toggle_public_private(request):
    list_id = request.GET.get('list_id', None)
    l = List.objects.filter(id=list_id)[0]
    l.public = False
    l.save()
    return JsonResponse({})


def like_list(request):
    list_id = request.GET.get('list_id', None)
    l = List.objects.filter(id=list_id)[0]
    if List.objects.filter(id=list_id, likers=request.user).count() > 0:
        l.likers.remove(request.user)
        return JsonResponse({'liked': False})
    l.likers.add(request.user)
    return JsonResponse({'liked': True})
