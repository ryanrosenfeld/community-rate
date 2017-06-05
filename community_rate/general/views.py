from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import *
from .models import *
import re

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

                return HttpResponseRedirect('/')

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


def home(request):
    if request.user.is_authenticated():
        return render(request, 'general/index.html', {'page': 'activity_feed'})
    else:
        return HttpResponseRedirect('/login/')


def docs(request):
    return render(request, 'material-dash-documentation.html')
