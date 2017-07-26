from .models import Notification


def collect_notifications(request):
    if request.user.is_authenticated():
        context_data = dict()
        context_data['notifications'] = Notification.objects.filter(user=request.user)[::-1]
        context_data['num_unread'] = len(Notification.objects.filter(user=request.user, is_read=False))
        return context_data
    return ''


def get_profile_pic_base_url(request):
    base_url = request.get_host()
    pic_url = "https://s3.amazonaws.com/communityrate-test/"
    if base_url == "www.community-rate.com" or base_url == "communityrate.herokuapp.com":
        pic_url = "https://s3.amazonaws.com/communityrate/"
    elif base_url == "communityrate-test.herokuapp.com":
        pic_url = "https://s3.amazonaws.com/communityrate-staging/"

    context_data = dict()
    context_data['profile_pic_base_url'] = pic_url
    return context_data
