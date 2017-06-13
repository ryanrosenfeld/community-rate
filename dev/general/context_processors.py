from .models import Notification


def collect_notifications(request):
    if request.user.is_authenticated():
        context_data = dict()
        context_data['notifications'] = Notification.objects.filter(user=request.user)[::-1]
        context_data['num_unread'] = len(Notification.objects.filter(user=request.user, is_read=False))
        return context_data
    return ''
