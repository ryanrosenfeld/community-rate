import binascii
import os
from threading import Timer

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
import boto3
import re

from general.services import send_email
from .forms import *
from .models import *
from .functions import collect_feed_updates
from users.forms import profileSetupForm
from community_rate.settings import BASE_DIR


User = get_user_model()


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
                return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return render(request, 'general/login.html', {'form': form, 'page': 'login'})


def fb_login(request):
    # Get passed in parameters
    first_name = request.GET.get('first_name', None)
    last_name = request.GET.get('last_name', None)
    email = request.GET.get('email', None)
    fb_id = request.GET.get('fb_id', None)

    # Check if user already exists in system w/ this fb id
    user = SiteUser.objects.filter(fb_id=fb_id)
    if len(user) > 0:
        user = user[0]
        login(request, user)
        return HttpResponseRedirect('/')

    # Check if matching user & assign fb id & login
    user = SiteUser.objects.filter(email=email)
    if len(user) > 0:
        user = user[0]
        user.fb_id = fb_id
        user.save()
        login(request, user)
        return HttpResponseRedirect('/')

    # If not, create new user & login
    username = first_name + "_" + last_name
    conflicts = SiteUser.objects.filter(username=username)
    if len(conflicts) > 0:
        num = 1
        while True:
            conflicts = SiteUser.objects.filter(username=username+num)
            if len(conflicts) > 0:
                num += 1
            else:
                username = username + num
                break
    user = SiteUser.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        fb_id=fb_id
    )
    user.save()
    login(request, user)
    return HttpResponseRedirect('/tutorial/')


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

            user = SiteUser.objects.create_user(username=username, password=password1,
                                                first_name=first, last_name=last,
                                                email=email)
            user.save()

            # Log the user in, take them to their homepage
            user = authenticate(username=username, password=password1)

            login(request, user)

            request.session['new-user'] = True
            return HttpResponseRedirect('/tutorial/')
    else:
        form = SignupForm()
    return render(request, 'general/register.html', {'form': form, 'page': 'register'})


def forgot_password(request):
    form = ForgotPasswordForm()
    message = ''

    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)

        if form.is_valid():
            u = SiteUser.objects.filter(email=request.POST['email'])
            if len(u) > 0:
                base_url = 'http://www.community-rate.com'
                u = u[0]
                u.reset_key = binascii.hexlify(os.urandom(24)).decode('utf-8')
                u.save()

                def reset_rk():
                    u.reset_key = '1'
                    u.save()

                # Reset reset_key after 5 minutes
                t = Timer(300.0, reset_rk)
                t.start()

                send_email('communityrate.help@gmail.com', 'CommunityRateMovies', u.email, 'CommunityRate Reset Password',
                           'Hello ' + u.first_name + ', please follow this link to reset your password: ' + base_url +
                           '/reset-password/' + u.reset_key + '/.\n\nUsername for your account:  ' + u.username)
                return HttpResponseRedirect('/login/')
            else:
                message = 'The email address could not be found in the system'
    return render(request, 'general/forgot-password.html', {'form': form, 'message': message})


def reset_password(request, key):
    form = ResetPassForm()
    message = ''
    key_check = SiteUser.objects.filter(reset_key=key)
    if len(key_check) == 0:
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        form = ResetPassForm(request.POST)
        if form.is_valid():
            if request.POST['password'] != request.POST['conf_password']:
                message = "The passwords did not match"
            else:
                u = SiteUser.objects.filter(username=request.POST['username'])
                if len(u) > 0:
                    u = u[0]
                    if key == u.reset_key and key != '1':
                        u.set_password(request.POST['password'])
                        u.reset_key = '1'
                        u.save()
                        return HttpResponseRedirect('/login/')
                    else:
                        message = "Invalid request"
    return render(request, 'reset-password.html', {'form': form, 'message': message, 'key': key})


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


@login_required
def activity_feed(request):
    # Get following users & append current user
    users = [follower_obj.following for follower_obj in request.user.follower_set.all()]
    users.append(request.user)

    # Collect updates in activity feed
    updates = collect_feed_updates(users)

    # Check if new user & show welcome message
    welcome = request.session.get('welcome', False)
    if welcome:
        request.session['welcome'] = None
    return render(request, 'activity-feed.html', {'updates': updates, 'page': 'activity_feed', 'welcome': welcome})


@login_required
def tutorial(request):
    form = profileSetupForm(initial={'timezone': 'US/Eastern'})
    new = request.session.get('new-user', False)
    if new:
        request.session['new-user'] = False
    if request.method == 'POST':
        form = profileSetupForm(request.POST)
        if form.is_valid():
            # Save profile changes
            about_me = form.cleaned_data['about_me']
            fav_quote = form.cleaned_data['fav_quote']
            timezone = form.cleaned_data['timezone']
            request.user.about_me = about_me
            request.user.fav_quote = fav_quote
            request.user.timezone = timezone
            request.user.save()

            request.session['welcome'] = True
            return HttpResponseRedirect('/activity-feed/')
    return render(request, 'general/tutorial.html', {'new_user': new,
                                                     'form': form})


@login_required
def welcome(request):
    return HttpResponseRedirect('/activity-feed/')


@login_required
def help_page(request):
    return render(request, 'help.html', {'page': 'help'})


@login_required
def contact(request):
    return render(request, 'contact.html', {'page': 'contact'})


@login_required
def sign_s3(request):
    file_name = str(request.user.id)
    file_type = request.GET.get('file_type', None)

    s3 = boto3.client('s3')

    bucket = "communityrate-test"
    base_url = request.get_host()
    if base_url == 'https://communityrate-test.herokuapp.com':
        bucket = "communityrate-staging"
    elif base_url == "http://www.community-rate.com" or base_url == "https://communityrate.herokuapp.com":
        bucket = "communityrate"

    presigned_post = s3.generate_presigned_post(
        Bucket=bucket,
        Key=file_name,
        Fields={"acl": "public-read", "Content-Type": file_type},
        Conditions=[
            {"acl": "public-read"},
            {"Content-Type": file_type}
        ],
        ExpiresIn=3600
    )

    return JsonResponse({
        'data': presigned_post,
        'url': 'https://communityrate.s3.amazonaws.com/' + file_name
    })
