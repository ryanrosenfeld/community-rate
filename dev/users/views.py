from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import *
from general.models import SiteUser
from movies.models import Review, List, ListEntry
from movies.services import get_movie_by_id


@login_required
def profile(request, user_id=""):
    """Public or private view of a person's profile"""
    if user_id == "":
        user = request.user
    else:
        try:
            user_id = int(user_id)
        except ValueError:
            return HttpResponseRedirect("/users/")

        try:
            user = SiteUser.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return HttpResponseRedirect("/users/")

    # Check if person requesting profile is the owner
    owner = user == request.user

    # Query reviews, length, ratings, lists
    reviews = Review.objects.filter(creator=user)
    number = len(reviews)
    avg = 0
    for r in reviews:
        r.movie = get_movie_by_id(r.movie_id, True)
        avg += r.rating

    if avg > 0:
        avg /= number
        avg = "{0:.1f}".format(avg)

    favorites = sorted(reviews, key=lambda x: x.rating, reverse=True)
    recents = sorted(reviews, key=lambda x: x.date_added, reverse=True)
    db_lists = List.objects.filter(creator=user)
    lists = []
    for l in db_lists:
        num_movies = len(ListEntry.objects.filter(list=l))
        likes = len(l.likers.all())
        lists.append((l, num_movies, likes))

    # Determine if this user is already following them OR
    # request user is actually this user
    following = request.user.follower_set.all()
    query = following.filter(following=user)
    already_following = (len(query) > 0) | owner

    # Determine page
    page = "users"
    if owner:
        page = "profile"

    # Get num followers & following
    num_following = len(user.follower_set.all())
    num_followers = len(user.following_set.all())

    # Collect form for editing info
    form = UpdateInfoForm(initial={'username': request.user.username, 'email': request.user.email,
                                   'first_name': request.user.first_name, 'last_name': request.user.last_name,
                                   'fav_quote': request.user.fav_quote, 'about_me': request.user.about_me})

    # If info updated make changes to user
    error_message = None
    if request.method == 'POST':
        form = UpdateInfoForm(request.POST)
        if form.is_valid():
            if request.POST['username'] != request.user.username and \
                    len(SiteUser.objects.filter(username=request.POST['username'])) > 0:
                error_message = "Sorry, the username you entered is already taken."
            elif form.cleaned_data['email'] != request.user.email and \
                    len(SiteUser.objects.filter(email=request.POST['email'])) > 0:
                error_message = "Sorry, the email you entered is already being used by an account."
            else:
                request.user.username = request.POST['username']
                request.user.email = request.POST['email']
                request.user.first_name = request.POST['first_name']
                request.user.last_name = request.POST['last_name']
                request.user.about_me = request.POST.get('about_me', None)
                request.user.fav_quote = request.POST.get('fav_quote', None)
                request.user.save()

    return render(request, 'users/profile.html', {
        'owner': owner,
        'num_reviews': number,
        'av_rating': avg,
        'favorites': favorites,
        'recents': recents,
        'page': page,
        'already_following': already_following,
        'user': user,
        'lists': lists,
        'form': form,
        'num_followers': num_followers,
        'num_following': num_following,
        'error_message': error_message})


@login_required
def settings(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST)
        if form.is_valid():

            # Iterate through form's fields
            for element in form.cleaned_data:
                val = form.cleaned_data[element]

                # Only update user's fields if it was set in form
                if val:
                    setattr(request.user, element, val)

            request.user.save()

            return HttpResponseRedirect('/profile/')

    form = EditProfileForm()
    return render(request, 'users/edit-profile.html', {
        'user': request.user,
        'settings': True,
        'form': form,
    })


@login_required
def main_view(request, response=None):
    """Main view for users page"""

    users = []

    # Find this user's followers, following
    following = request.user.follower_set.all()
    # for index, f in enumerate(following):
    #     following[index] = f.following
    # user = following[0].following
    # print(user.get_full_name)

    followers = request.user.following_set.all()

    # Retrieve all users
    all_users = SiteUser.objects.all()

    # Append their follower count and
    # whether or not they are already following that person
    for user in all_users:
        # Find follower count
        followers_count = len(user.following_set.all())

        # Determine if this user is already following them OR
        # request user is actually this user
        query = following.filter(following=user)
        already_following = (len(query) > 0) | (user == request.user)

        users.append((user, followers_count, already_following))

    # Sort by follower count (highest first)
    users = sorted(users, key=lambda x: x[1], reverse=True)

    # Set display variables for 'main' view
    title = "Top Users"
    comment = "Find new favorites!"

    return render(request, 'users/main.html', {'num_followers': len(followers),
                                               'num_following': len(following),
                                               'users': users,
                                               'response': response,
                                               'title': title,
                                               'comment': comment,
                                               'page': 'all_users',
                                               'followers': followers,
                                               'following': following})


@login_required
def relationships(request, user_id=""):
    """View for page that displays all of the users that a particular user is following"""
    if user_id == "":
        user = request.user
    else:
        user = SiteUser.objects.filter(id=user_id)
        if len(user) > 0:
            user = user[0]
        else:
            return HttpResponseRedirect("/users/")

    owner = user == request.user
    if owner:
        page = "relationships"
    else:
        page = "users"

    following_users = []
    follower_users = []

    # Query all of the users this person is following
    following = user.follower_set.all()
    followers = user.following_set.all()

    for follower_obj in following:
        # Determine follower count of person they are FOLLOWING (this is messy)
        followers_count = len(follower_obj.following.following_set.all())
        already_following = True
        following_users.append((follower_obj.following, followers_count, already_following))

    for follower_obj in followers:
        # Determine follower count of person that follow them (this is messy)
        followers_count = len(follower_obj.follower.following_set.all())

        # Determine if this user is already following them OR
        # request user is actually this user
        query = following.filter(following=follower_obj.follower)
        already_following = (len(query) > 0) | (follower_obj.follower == user)

        follower_users.append((follower_obj.follower, followers_count, already_following))

    return render(request, 'users/relationships.html', {
        'num_followers': len(followers),
        'num_following': len(following),
        'following_users': following_users,
        'follower_users': follower_users,
        'page': page,
        'user': user,
        'owner': owner})
