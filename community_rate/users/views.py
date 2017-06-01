from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import render
from .forms import *
from .models import *
from general.models import SiteUser, Notification
from movies.models import Review, List
from movies.services import get_movie_by_id
from .functions import *
from random import randint

@login_required
def profile(request, username=""):
    """Public or private view of a person's profile"""
    if username == "":
        user = request.user
    else:
        try:
            user = SiteUser.objects.get(username=username)

        except ObjectDoesNotExist:
            response = "User \"{0}\" does not exist".format(username)
            return main_view(request, response)

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
    lists = List.objects.filter(creator=user)

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

    picform = UpdateProfilePicForm()

    # If info updated make changes to user
    if request.method == 'POST':
        if 'email' in request.POST:
            form = UpdateInfoForm(initial={'username': request.user.username, 'email': request.POST['email'],
                                           'first_name': request.POST['first_name'],
                                           'last_name': request.POST['last_name'],
                                           'fav_quote': request.POST['fav_quote'],
                                           'about_me': request.POST['about_me']})
            # ADD IS_VALID CHECK?
            request.user.email = request.POST['email']
            request.user.first_name = request.POST['first_name']
            request.user.last_name = request.POST['last_name']
            request.user.about_me = request.POST.get('about_me', None)
            request.user.fav_quote = request.POST.get('fav_quote', None)
            request.user.save()
        elif 'file' in request.FILES:
            picform = UpdateProfilePicForm(request.POST, request.FILES)
            # if picform.is_valid():
            file = request.FILES['file']
            print(file)
            upload_prof_pic(file, request.user)

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
        'picform': picform,
        'num_followers': num_followers,
        'num_following': num_following})


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
                                               'page': 'users',
                                               'followers': followers,
                                               'following': following})


@login_required
def follow(request, username):
    """Creates follow connection between requester and person they wish to follow"""

    # Retrieve the SiteUser account of the person they wish to follow
    try:
        following_user = SiteUser.objects.get(username=username)

    except ObjectDoesNotExist:
        response = "User \"{0}\" does not exist".format(username)
        return main_view(request, response)

    # Determine if this user is already following them
    query = request.user.follower_set.filter(following=following_user)
    already_following = len(query) > 0

    if already_following:
        response = "You are already following {0}!".format(username)
        return main_view(request, response)

    # Person exists and this user is not already following them
    f = Follower.objects.create(follower=request.user, following=following_user)
    f.save()

    # Create a notification for the person who was followed
    msg = "{0} is now following you!".format(request.user.username)
    n = Notification.objects.create(message=msg, notification_class="Follower", user=following_user)
    n.save()

    # Provide response for requester, return
    response = "You are now following {0}".format(username)
    return main_view(request, response)


@login_required
def relationships(request):
    """View for page that displays all of the users that a particular user is following"""
    following_users = []
    follower_users = []

    # Query all of the users this person is following
    following = request.user.follower_set.all()
    followers = request.user.following_set.all()

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
        already_following = (len(query) > 0) | (follower_obj.follower == request.user)

        follower_users.append((follower_obj.follower, followers_count, already_following))

    return render(request, 'users/relationships.html', {
        'num_followers': len(followers),
        'num_following': len(following),
        'following_users': following_users,
        'follower_users': follower_users,
        'page': 'relationships'})


# @login_required
# def view_followers(request):
#     """View for page that displays all of the users that follow a particular user"""
#     users = []
#
#     # Query all of the users this person is following
#     following = request.user.follower_set.all()
#
#     followers = request.user.following_set.all()
#
#     # Append their follower count and
#     # whether or not they are already following that person
#     for follower_obj in followers:
#         # Determine follower count of person that follow them (this is messy)
#         followers_count = len(follower_obj.follower.following_set.all())
#
#         # Determine if this user is already following them OR
#         # request user is actually this user
#         query = following.filter(following=follower_obj.follower)
#         already_following = (len(query) > 0) | (follower_obj.follower == request.user)
#
#         users.append((follower_obj.follower, followers_count, already_following))
#
#     # Set up the display variables for the 'following' view
#     title = "Your Followers"
#
#     # Retrieve notifications
#     notifications = Notification.objects.filter(Q(user=request.user) & Q(is_read=False))
#
#     return render(request, 'users/relationships.html', {
#         'num_followers': len(followers),
#         'num_following': len(following),
#         'users': users,
#         'title': title,
#         'notifications': notifications,
#         'number_notifications': len(notifications)})
