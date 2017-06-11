import pytz

from django.utils import timezone
from general.models import Notification


class TimezoneMiddleware(object):
    def process_request(self, request):
        try:
            timezone.activate(pytz.timezone(request.user.timezone))
        except AttributeError:
            timezone.activate(pytz.timezone("US/Eastern"))


class Notifications(object):
    def process_response(self, request, response):
        print("HERE")
        n = Notification.objects.filter(user=request.user)
        if len(n) > 0:
            response.context_data['notifications'] = n
        return response
