from django.http import JsonResponse

from general.models import SiteUser, Notification
from movies.functions import get_following_user_reviews, calc_average_review
from movies.models import Review, ListEntry, List
from movies.services import get_movie_by_id, search_movies


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
    l.public = not l.public
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


def add_editor(request):
    list_id = request.GET.get('list_id', None)
    l = List.objects.filter(id=list_id)[0]

    user_id = request.GET.get('user_id', None)
    user = SiteUser.objects.filter(id=user_id)[0]

    l.editors.add(user)

    # Add a notification
    msg = "{0} {1} added you as an editor on the list {2}".format(request.user.first_name, request.user.last_name,
                                                                   l.name)
    url = "/list/" + list_id + "/"
    n = Notification.objects.create(message=msg, url=url, user=user)
    n.save()
    return JsonResponse({})


def remove_editor(request):
    list_id = request.GET.get('list_id', None)
    l = List.objects.filter(id=list_id)[0]

    user_id = request.GET.get('user_id', None)
    user = SiteUser.objects.filter(id=user_id)[0]

    l.editors.remove(user)
    return JsonResponse({})