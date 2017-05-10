from django.conf.urls import url
from django.contrib import admin
from general import views as general_views
from movies import views as movie_views
from users import views as user_views

urlpatterns = [
    url(r'^$', general_views.home),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', general_views.login_view),
    url(r'^signup/', general_views.new_user),
    url(r'^logout/', general_views.logout_view),
    url(r'^search/', movie_views.search),
    url(r'^movie/(.*)/', movie_views.movie_page),
    url(r'^movies/', movie_views.movie_db),

    # Users views
    url(r'^users/', user_views.main_view),
    url(r'^all_users/', user_views.view_users),
    url(r'^follow/(?P<username>\w{0,50})/$', user_views.follow),
    url(r'^profile/', user_views.profile),

    # AJAX Requests
    url(r'^ajax/filter-movies/', movie_views.filter_movies),
    url(r'^ajax/get-movie-rating/', movie_views.get_movie_rating),
]
