from django.conf.urls import url
from django.contrib import admin
from general import views as general_views, ajax as general_ajax
from movies import views as movie_views, ajax as movie_ajax
from users import views as user_views, ajax as user_ajax

urlpatterns = [
    # General views
    url(r'^$', general_views.home),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', general_views.login_view),
    url(r'fb-login/', general_views.fb_login),
    url(r'^register/$', general_views.new_user),
    url(r'^forgot-password/', general_views.forgot_password),
    url(r'^reset-password/(.*)/', general_views.reset_password),
    url(r'^logout/', general_views.logout_view),
    url(r'^accounts/login/$', general_views.login_view, name='login'),
    url(r'^activity-feed/', general_views.activity_feed),
    url(r'^help/', general_views.help_page),
    url(r'^contact/', general_views.contact),
    url(r'^read/(?P<notification_id>\w{0,50})/$', general_views.mark_read),
    url(r'^show-welcome/', general_views.show_welcome),
    url(r'^hide-welcome/', general_views.hide_welcome),

    # Movie views
    url(r'^movie/(.*)/', movie_views.movie_page),
    url(r'^movies/', movie_views.movie_db),
    url(r'^top-movies/', movie_views.top_movies),
    url(r'^my-reviews/', movie_views.my_reviews),
    url(r'^lists/', movie_views.lists),
    url(r'^list/(.*)/delete/', movie_views.delete_list),
    url(r'^list/(.*)/', movie_views.list_page),
    url(r'^new-list/', movie_views.new_list),

    # Users views
    url(r'^users/', user_views.main_view),
    url(r'^follow/(?P<user_id>\w{0,50})/$', user_ajax.follow),
    url(r'^profile/(?P<user_id>\w{0,50})/$', user_views.profile),
    url(r'^profile/$', user_views.profile),
    url(r'^relationships/(?P<user_id>\w{0,50})/$', user_views.relationships),


    # AJAX URLs -------------------------------------------------

    # General AJAX Requests
    url(r'^ajax/mark-notifications-read/', general_ajax.mark_notifications_read),
    url(r'^ajax/add-comment/', general_ajax.add_comment),
    url(r'^ajax/hide-welcome/', general_ajax.hide_welcome),
    url(r'^ajax/show-welcome/', general_ajax.show_welcome),

    # Movie AJAX Requests
    url(r'^ajax/filter-movies/', movie_ajax.filter_movies),
    url(r'^ajax/get-movie-rating/', movie_ajax.get_movie_rating),
    url(r'^ajax/get-movie-info/', movie_ajax.get_movie_info),
    url(r'^ajax/add-list-entry/', movie_ajax.add_list_entry),
    url(r'^ajax/update-list-name/', movie_ajax.update_list_name),
    url(r'^ajax/remove-list-item/', movie_ajax.remove_list_item),
    url(r'^ajax/toggle-public-private/', movie_ajax.toggle_public_private),
    url(r'^ajax/like-list/', movie_ajax.like_list),
    url(r'^ajax/add-editor/', movie_ajax.add_editor),
    url(r'^ajax/remove-editor/', movie_ajax.remove_editor),

    # User AJAX Requests
    url(r'^ajax/follow/', user_ajax.follow),
    url(r'^ajax/unfollow/', user_ajax.unfollow),
    url(r'^ajax/has-pic/', user_ajax.has_pic),
    url(r'^ajax/upload-profile-pic/', user_ajax.upload_profile_pic)
]
