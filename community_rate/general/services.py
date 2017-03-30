import requests


api_key = 'fd8332d364611c30a611272eb023f170'


def search_movies(query):
    url = 'https://api.themoviedb.org/3/search/movie'
    params = {'api_key': api_key, 'query': query}
    r = requests.get(url, params=params)
    movies = r.json()
    return movies


def get_movie_by_id(id):
    url = "https://api.themoviedb.org/3/movie/" + id + "?language=en-US&api_key=" + api_key
    r = requests.get(url)
    movie = r.json()
    return movie
