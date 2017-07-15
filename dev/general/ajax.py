from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from general.models import Notification
from movies.models import Review, Comment


@login_required
def mark_notifications_read(request):
    notes = Notification.objects.filter(user=request.user, is_read=False)
    for n in notes:
        n.is_read = True
        n.save()
    return JsonResponse({})


@login_required
def add_comment(request):
    # Get passed in parameters
    review_id = request.GET.get('review_id', None)
    comment = request.GET.get('comment', None)
    if review_id is None or comment is None:
        return JsonResponse({})

    review = Review.objects.get(id=int(review_id))
    comment = Comment(review=review, author=request.user, comment=comment)
    comment.save()
    return JsonResponse({})
