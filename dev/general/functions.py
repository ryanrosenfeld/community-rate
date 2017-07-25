from movies.models import Review, Comment
from movies.services import get_movie_by_id


def collect_feed_updates(users):
    updates = []
    for user in users:
        reviews = Review.objects.filter(creator=user)
        for r in reviews:
            movie = get_movie_by_id(r.movie_id, True)
            comments = Comment.objects.filter(review=r)
            comments = sorted(comments, key=lambda x: x.date_added, reverse=True)
            updates.append((user, movie, r, comments))
    updates = sorted(updates, key=lambda x: x[2].date_added, reverse=True)
    return updates
