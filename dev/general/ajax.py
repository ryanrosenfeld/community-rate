from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from general.models import Notification
from movies.models import Review, Comment
from movies.services import get_movie_by_id


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

    # Create a new comment object
    review = Review.objects.get(id=int(review_id))
    comment = Comment(review=review, author=request.user, comment=comment)
    comment.save()

    # Add a notification
    movie = get_movie_by_id(review.movie_id, False)
    msg = "{0} {1} made a comment on your review of {2}".format(request.user.first_name, request.user.last_name,
                                                                 movie['title'])
    url = "/my-reviews/#review-" + review_id
    n = Notification.objects.create(message=msg, url=url, user=review.creator)
    n.save()
    return JsonResponse({})
