from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from general.models import SiteUser, Notification
from users.models import Follower


@login_required
def follow(request):
    """Creates follow connection between requester and person they wish to follow"""
    print("Following...")
    # Get username
    username = request.GET.get('username', None)
    if username is None:
        return JsonResponse({})
    print(username)

    # Retrieve the SiteUser account of the person they wish to follow
    try:
        following_user = SiteUser.objects.get(username=username)
    except ObjectDoesNotExist:
        return JsonResponse({})
    print(following_user)

    # Determine if this user is already following them
    query = request.user.follower_set.filter(following=following_user)
    already_following = len(query) > 0
    print(already_following)
    if already_following:
        return JsonResponse({})
    print(already_following)

    # Person exists and this user is not already following them
    f = Follower.objects.create(follower=request.user, following=following_user)
    f.save()

    # Create a notification for the person who was followed
    msg = "{0} {1} is now following you!".format(request.user.first_name, request.user.last_name)
    n = Notification.objects.create(message=msg, notification_class="Follower", user=following_user)
    n.save()
    return JsonResponse({'success': True})


@login_required
def unfollow(request):
    """Creates follow connection between requester and person they wish to follow"""
    print("Unfollowing...")
    # Get username
    username = request.GET.get('username', None)
    if username is None:
        return JsonResponse({})
    print(username)

    # Retrieve the SiteUser account of the person they wish to follow
    try:
        following_user = SiteUser.objects.get(username=username)
    except ObjectDoesNotExist:
        return JsonResponse({})
    print(following_user)

    # Determine if this user is already following them
    query = request.user.follower_set.filter(following=following_user)
    already_following = len(query) > 0
    if not already_following:
        return JsonResponse({})
    print(already_following)

    # If person exists and this user is following them delete Follower object
    f = ''
    try:
        f = Follower.objects.get(follower=request.user, following=following_user)
    except ObjectDoesNotExist:
        return JsonResponse({})
    print(f)
    f.delete()

    return JsonResponse({'success': True})