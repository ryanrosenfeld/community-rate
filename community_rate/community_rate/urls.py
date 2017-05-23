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
    url(r'^profile/', user_views.profile),
    url(r'^movies/', movie_views.movie_db),
    url(r'^new-list/', movie_views.new_list),
    url(r'^edit-list/(.*)/', movie_views.edit_list),
    # url(r'^users/', user_views.users),

    # AJAX Requests
    url(r'^ajax/filter-movies/', movie_views.filter_movies),
    url(r'^ajax/get-movie-rating/', movie_views.get_movie_rating),
    url(r'^ajax/get-movie-info/', movie_views.get_movie_info),
    url(r'^ajax/add-list-entry/', movie_views.add_list_entry),
]
