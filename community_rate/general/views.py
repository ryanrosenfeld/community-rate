from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import SiteUser
from django.contrib.auth import authenticate, login, logout

from .forms import *
from .services import *


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
    return render(request, 'login.html', {'form': form})


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
    return render(request, 'signup.html', {'form': form})


def home(request):
    if request.user.is_authenticated():
        return render(request, 'index.html')
    else:
        return HttpResponseRedirect('/login/')


def search(request):
    if request.method == 'GET':
        s = request.GET.get('search', None)
        if s is not None:
            movies = search_movies(s)
            return render(request, 'search-results.html', {'movies': movies})
    else:
        return HttpResponseRedirect('/')


def movie_page(request, id):
    movie = get_movie_by_id(id)
    form = ReviewForm()
    return render(request, 'movie.html', {'movie': movie, 'form': form})


def profile(request):
    return render(request, 'profile.html')
