from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from general.models import SiteUser, Notification
from users.models import Follower


@login_required
def follow(request):
    """Creates follow connection between requester and person they wish to follow"""
    # Get username
    username = request.GET.get('username', None)
    if username is None:
        return JsonResponse({})

    # Retrieve the SiteUser account of the person they wish to follow
    try:
        following_user = SiteUser.objects.get(username=username)
    except ObjectDoesNotExist:
        return JsonResponse({})

    # Determine if this user is already following them
    query = request.user.follower_set.filter(following=following_user)
    already_following = len(query) > 0

    if already_following:
        return JsonResponse({})

    # Person exists and this user is not already following them
    f = Follower.objects.create(follower=request.user, following=following_user)
    f.save()

    # Create a notification for the person who was followed
    msg = "{0} {1} is now following you".format(request.user.first_name, request.user.last_name)
    url = "/profile/" + str(request.user.id) + "/"
    n = Notification.objects.create(message=msg, url=url, user=following_user)
    n.save()
    return JsonResponse({'success': True})


@login_required
def unfollow(request):
    """Creates follow connection between requester and person they wish to follow"""
    # Get username
    username = request.GET.get('username', None)
    if username is None:
        return JsonResponse({})

    # Retrieve the SiteUser account of the person they wish to follow
    try:
        following_user = SiteUser.objects.get(username=username)
    except ObjectDoesNotExist:
        return JsonResponse({})

    # Determine if this user is already following them
    query = request.user.follower_set.filter(following=following_user)
    already_following = len(query) > 0
    if not already_following:
        return JsonResponse({})

    # If person exists and this user is following them delete Follower object
    f = ''
    try:
        f = Follower.objects.get(follower=request.user, following=following_user)
    except ObjectDoesNotExist:
        return JsonResponse({})

    f.delete()

    return JsonResponse({'success': True})


@login_required
def has_pic(request):
    request.user.has_pic = True
    request.user.save()
    return JsonResponse({})


@login_required
def upload_profile_pic(request):
    pic = request.POST.get('pic', None)
    if pic is None:
        return JsonResponse({})

    print(pic)
    request.user.profile_pic = pic
    request.user.save()
    return JsonResponse({})
