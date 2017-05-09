from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import *
from .models import SiteUser


# Create your views here.
def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print("form valid")
            u = request.POST['username']
            p = request.POST['password']
            user = authenticate(username=u, password=p)
            print("HERE")
            if user is not None:
                print("Logging in")
                login(request, user)
                request.user.remember = request.POST.get('remember', False)
                return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return render(request, 'general/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def new_user(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = SiteUser.objects.create_user(request.POST['username'], request.POST['email'],
                                                request.POST['password'])
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
            return HttpResponseRedirect('/login/')
    else:
        form = SignupForm()
    return render(request, 'general/signup.html', {'form': form})


def home(request):
    if request.user.is_authenticated():
        return render(request, 'general/index.html', {'page': 'activity_feed'})
    else:
        return HttpResponseRedirect('/login/')
