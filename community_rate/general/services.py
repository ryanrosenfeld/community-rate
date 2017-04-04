import requests


api_key = 'fd8332d364611c30a611272eb023f170'


def search_movies(query):
    url = 'https://api.themoviedb.org/3/search/movie'
    params = {'api_key': api_key, 'query': query}
    r = requests.get(url, params=params)
    movies = r.json()
    return movies


def get_movie_by_id(movie_id):
    url = "https://api.themoviedb.org/3/movie/" + str(movie_id) + "?language=en-US&api_key=" + api_key
    r = requests.get(url)
    movie = r.json()
    # movie.img = get_poster_img(movie, 'w92')
    return movie


def get_poster_img(movie, size):
    print(movie.title)
    url = "http://image.tmdb.org/t/p/" + size + movie.poster_path
    r = requests.get(url)
    return r.json()
