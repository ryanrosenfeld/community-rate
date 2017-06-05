from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from general import views as general_views
from movies import views as movie_views
from users import views as user_views
from community_rate import settings

urlpatterns = [
    # General views
    url(r'^$', general_views.home),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', general_views.login_view),
    url(r'^register/$', general_views.new_user),
    url(r'^logout/', general_views.logout_view),
    url(r'^accounts/login/$', general_views.login_view, name='login'),
    url(r'^read/(?P<notification_id>\w{0,50})/$', general_views.mark_read),

    # Movie views
    url(r'^search/', movie_views.search),
    url(r'^movie/(.*)/', movie_views.movie_page),
    url(r'^movies/', movie_views.movie_db),
    url(r'^lists/', movie_views.lists),
    url(r'^list/(.*)/', movie_views.list_page),
    url(r'^new-list/', movie_views.new_list),
    url(r'^edit-list/(.*)/', movie_views.edit_list),

    # Users views
    url(r'^users/', user_views.main_view),
    url(r'^follow/(?P<username>\w{0,50})/$', user_views.follow),
    url(r'^profile/(?P<username>\w{0,50})/$', user_views.profile),
    url(r'^profile/$', user_views.profile),
    url(r'^settings/$', user_views.settings),
    url(r'^relationships/$', user_views.relationships),

    # Movie AJAX Requests
    url(r'^ajax/filter-movies/', movie_views.filter_movies),
    url(r'^ajax/get-movie-rating/', movie_views.get_movie_rating),
    url(r'^ajax/get-movie-info/', movie_views.get_movie_info),
    url(r'^ajax/add-list-entry/', movie_views.add_list_entry),
    url(r'^ajax/update-list-name/', movie_views.update_list_name),
    url(r'^ajax/remove-list-item/', movie_views.remove_list_item),
    url(r'^ajax/toggle-public-private/', movie_views.toggle_public_private),
    url(r'^ajax/like-list/', movie_views.like_list),

    # User AJAX Requests
    url(r'^ajax/follow/', user_views.follow),
    url(r'^ajax/unfollow/', user_views.unfollow),

    url(r'^documentation/$', general_views.docs),
]
