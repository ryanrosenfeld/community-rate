from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from general.models import Notification


@login_required
def mark_notifications_read(request):
    notes = Notification.objects.filter(user=request.user, is_read=False)
    for n in notes:
        n.is_read = True
        n.save()
    return JsonResponse({})
