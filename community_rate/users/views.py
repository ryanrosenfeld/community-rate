from django.shortcuts import render
from movies.models import Review, List
from movies.services import get_movie_by_id
from .forms import UpdateInfoForm


def profile(request):
    reviews = Review.objects.filter(user_id=request.user.id)
    for r in reviews:
        r.movie = get_movie_by_id(r.movie_id, True)
    num_reviews = len(reviews)
    av_rating = 0
    if num_reviews > 0:
        av_rating = "{0:.1f}".format(sum(r.rating for r in reviews) / len(reviews))
    favorites = sorted(reviews, key=lambda x: x.rating, reverse=True)
    recents = sorted(reviews, key=lambda x: x.date_added, reverse=True)
    lists = List.objects.filter(creator=request.user)
    form = UpdateInfoForm(initial={'username': request.user.username, 'email': request.user.email,
                                   'first_name': request.user.first_name, 'last_name': request.user.last_name,
                                   'fav_quote': request.user.fav_quote, 'about_me': request.user.about_me})
    if request.method == 'POST':
        form = UpdateInfoForm(initial={'username': request.user.username, 'email': request.POST['email'],
                                       'first_name': request.POST['first_name'], 'last_name': request.POST['last_name'],
                                       'fav_quote': request.POST['fav_quote'], 'about_me': request.POST['about_me']})
        # ADD IS_VALID CHECK?
        request.user.email = request.POST['email']
        request.user.first_name = request.POST['first_name']
        request.user.last_name = request.POST['last_name']
        request.user.about_me = request.POST.get('about_me', None)
        request.user.fav_quote = request.POST.get('fav_quote', None)
        request.user.save()
    return render(request, 'my-profile.html', {'favorites': favorites, 'recents': recents, 'lists': lists,
                                               'page': 'profile', 'form': form, 'num_reviews': num_reviews,
                                               'av_rating': av_rating})
