import pytz

from django.utils import timezone


class TimezoneMiddleware(object):
    def process_request(self, request):
        try:
            timezone.activate(pytz.timezone(request.user.timezone))
        except AttributeError:
            timezone.activate(pytz.timezone("US/Eastern"))
