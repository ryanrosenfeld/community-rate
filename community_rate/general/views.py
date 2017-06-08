from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import *
from .models import *
from movies.models import Review
from movies.services import get_movie_by_id
import re
from users.forms import profileSetupForm
from users.functions import upload_prof_pic

User = get_user_model()

# Create your views here.
def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():

            u = request.POST['username']
            p = request.POST['password']
            user = authenticate(username=u, password=p)
            
            if user is not None:

                login(request, user)
                request.user.remember = request.POST.get('remember', False)
                return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return render(request, 'general/login.html', {'form': form, 'page': 'login'})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def verify_username(username):
    """Verifies that the username has the required regular expression structure and is unique."""
    if not re.search(r'^\w+$', username):
        return False
    try:
        SiteUser.objects.get(username__iexact=username)
    except ObjectDoesNotExist:
        return True
    return False


def passwords_match(password1, password2):
    """Checks to make sure the entered passwords agree."""
    return password1 == password2


def new_user(request):
    """Create a new user"""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Grab cleaned data from form
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password']
            password2 = form.cleaned_data['conf_password']
            first = form.cleaned_data['first_name']
            last = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            # Check username, passwords (may want to also check emails)
            if verify_username(username) and passwords_match(password1, password2):
                # Create new (site) user object
                user = User.objects.create_user(username=username, 
                    password=password1,
                    first_name=first,
                    last_name=last,
                    email=email)
                user.save()
                
                # Log the user in, take them to their homepage
                user = authenticate(username=username, password=password1)

                login(request, user)

                request.session['new-user'] = True
                return HttpResponseRedirect('/tutorial/')

            return HttpResponseRedirect('/register/')
    else:
        form = SignupForm()
    return render(request, 'general/register.html', {'form': form, 'page': 'register'})


@login_required
def mark_read(request, notification_id):
    """If user has access to this notification, mark it as read"""
    try:
        notification = Notification.objects.get(id=notification_id)
    except ObjectDoesNotExist:
        raise Http404

    if notification.user != request.user:
        # TODO: raise security message instead
        raise Http404
    else:
        notification.is_read = True
        notification.save()


@login_required
def home(request):
    return HttpResponseRedirect('/activity-feed/')


def activity_feed(request):
    # Get following users
    following = request.user.follower_set.all()
    updates = []
    for follower_obj in following:
        reviews = Review.objects.filter(creator=follower_obj.following)
        for r in reviews:
            movie = get_movie_by_id(r.movie_id, True)
            updates.append((follower_obj.following, movie, r))
    updates = sorted(updates, key=lambda x: x[2].date_added, reverse=True)

    welcome = request.session.get('welcome', False)
    if welcome:
        request.session['welcome'] = None
    return render(request, 'activity-feed.html', {'updates': updates, 'page': 'activity_feed', 'welcome': welcome})


@login_required
def tutorial(request):
    form = profileSetupForm()
    new = request.session.get('new-user', False)
    if new:
        request.session['new-user'] = False
    if request.method == 'POST':
        form = profileSetupForm(request.POST, request.FILES)
        if form.is_valid():
            about_me = form.cleaned_data['about_me']
            fav_quote = form.cleaned_data['fav_quote']
            request.user.about_me = about_me
            request.user.fav_quote = fav_quote
            request.user.save()

            prof_pic = request.FILES['prof_pic']
            upload_prof_pic(prof_pic, request.user)
            request.session['welcome'] = True
            return HttpResponseRedirect('/activity-feed/')
    return render(request, 'general/tutorial.html', {'new_user': new,
                                                     'form': form})


@login_required
def welcome(request):
    return HttpResponseRedirect('/activity-feed/')
