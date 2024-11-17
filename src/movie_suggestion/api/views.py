from django.shortcuts import render
import requests
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from movie_suggestion.settings import TMDB_API_KEY, TMDB_API_URL
from api.models import Genre, MovieRecommendation, User
import re

# Mock the user selection for Genre
GENRE_LIST = [18, 28]


def index(request):
    return HttpResponse("Your API is running!")


def sanitize_query_params(params):
    """Sanitizes query parameters to prevent SQL injection."""
    sanitized_params = {}

    for key, value in params.items():
        if isinstance(value, str):
            # Remove unwanted characters
            sanitized_value = re.sub(r'[^a-zA-Z0-9\s]', '', value)
            sanitized_params[key] = sanitized_value.strip()  # Remove whitespace
        else:
            # If not a string, just add to the dictionary
            sanitized_params[key] = value

    return sanitized_params


def make_tmdb_request(endpoint, params=None):
    """Helper function to make requests to the TMDB API."""
    url = f"{TMDB_API_URL}/{endpoint}"
    headers = {
        "accept": "application/json",
        "Authorization": TMDB_API_KEY
    }
    response = requests.get(url, headers=headers, params=params)

    # Return data and status_code in all cases
    if response.status_code == 200:
        return response.json(), 200
    else:
        return {'error': f"Failed to fetch data: {response.status_code}"}, response.status_code


@api_view(['GET'])
def get_recommended_movie(request):
    ''' Get recommended movie
        http://127.0.0.1:8000/api/movies/recommended/

    '''
    params = {
        'page': '1',
        'language': 'en-US',
        'sort_by': 'popularity.desc',
        'include_adult': 'false',
        'include_video': 'false',
        'with_genres': ','.join(map(str, GENRE_LIST)), # TODO: Get list from logged user.
        'vote_average.gte': '9'
    }
    user = User.objects.get(id=1) # TODO: Get user from session

    data, status_code = make_tmdb_request("discover/movie", params)
    if status_code == 200:
        MovieRecommendation.add_recommendation(user, data['results'][0])

    movie = MovieRecommendation.objects.all().values('title', 'voteAverage')
    movie_list = list(movie)  # Convert QuerySet to list of dictionaries
    return JsonResponse(movie_list, safe=False)


# @api_view(['GET'])
def get_movies_genre(request):
    force = request.GET.get('force', 'false').lower() == 'true' # Force populating database

    if force or not Genre.objects.exists():
        params = {'language': 'en-US'}
        data, status_code = make_tmdb_request("genre/movie/list", params)
        if status_code == 200:
            Genre.populate(data['genres'])
    genres = Genre.objects.all().values('id', 'name')  # Retrieve genres as dictionaries
    genres_list = list(genres)  # Convert QuerySet to list of dictionaries
    return JsonResponse(genres_list, safe=False)


@api_view(['GET'])
def fetch_movies(request):
    # Capture all parameters from the GET request
    params = request.GET.dict()  # Get all parameters as a dictionary

    # Sanitize parameters
    sanitized_params = sanitize_query_params(params)
    # Check if the 'query' parameter was provided
    if 'query' not in sanitized_params or not sanitized_params['query']:
        return JsonResponse({'error': 'Query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

    data, status_code = make_tmdb_request("search/multi", sanitized_params)
    return JsonResponse(data, safe=False, status=status_code)


# @api_view(['GET'])
# def tmdb_fetch_movies2(request):
#     params = {
#         'append_to_response': 'images',
#         'language': 'en-US',
#         'include_image_language': 'en,null'
#     }
#     data, status_code = make_tmdb_request("movie/550", params)
#     return JsonResponse(data, safe=False, status=status_code)
#

@api_view(['GET'])
def tmdb_movie_details(request):

    # https://api.themoviedb.org/3/movie/874538?language=en-US

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0ZDUyZGYwYTYxNDIyZjZkZmFjMTNiZGE4NzA3OTQxMSIsIm5iZiI6MTczMTM3MjE1MS45OTU0NjM0LCJzdWIiOiI2NzI5NjM0NTUwZTE1ZThmNWE1ODA1ZGYiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.WvQbFDlTfJQLZq2mYJxbrcYSpBGprTvVJgiQCcJSAO0"
    }

    # Capture all parameters from the GET request
    params = request.GET.dict()  # Get all parameters as a dictionary

    # Sanitize parameters
    sanitized_params = sanitize_query_params(params)
    # Check if the 'query' parameter was provided
    if 'query' not in sanitized_params or not sanitized_params['query']:
        return JsonResponse({'error': 'Query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

    data, status_code = make_tmdb_request("search/multi", sanitized_params)
    return JsonResponse(data, safe=False, status=status_code)