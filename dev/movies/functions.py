from .models import Review
from general.common_functions import most_common


def get_following_user_reviews(user, movie_id):
    # Get following users
    following = user.follower_set.all()
    following_users = []
    for follower_obj in following:
        try:
            rev = Review.objects.get(movie_id=movie_id, creator=follower_obj.following)
        except Review.DoesNotExist:
            rev = None
        if rev is not None:
            following_users.append((follower_obj.following, rev))
    return following_users


def calc_average_review(user_revs):
    av_rating = ''
    most_common_react = ''
    if len(user_revs) > 0:
        # Calculate average rating
        av_rating = float(sum(r.rating for u, r in user_revs)) / len(user_revs)
        av_rating = "{0:.1f}".format(av_rating)

        # Get most common reaction
        reactions = []
        for u, rev in user_revs:
            reactions.append(rev.reaction)
        most_common_react = most_common(reactions)

    return av_rating, most_common_react
