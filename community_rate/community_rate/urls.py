from django.conf.urls import url
from django.contrib import admin
from general import views as general_views

urlpatterns = [
    url(r'^$', general_views.home),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', general_views.login_view),
    url(r'^signup/', general_views.new_user),
    url(r'^logout/', general_views.logout_view),
    url(r'^search/', general_views.search),
    url(r'^movie/(.*)/', general_views.movie_page),
    url(r'^profile/', general_views.profile),
]
