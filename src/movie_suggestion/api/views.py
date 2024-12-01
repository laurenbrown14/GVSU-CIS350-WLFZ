from django.shortcuts import render
import requests
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from movie_suggestion.settings import TMDB_API_KEY, TMDB_API_URL
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
def get_suggestion_list(request):
    params = {
        'page': '1',
        'language': 'en-US',
        'sort_by': 'popularity.desc',
        'include_adult': 'false',
        'include_video': 'false',
        'with_genres': ','.join(map(str, GENRE_LIST)),
        'vote_average.gte': '9'
    }
    data, status_code = make_tmdb_request("discover/movie", params)
    return JsonResponse(data, safe=False, status=status_code)


@api_view(['GET'])
def get_movies_genre(request):
    params = {'language': 'en-US'}
    data, status_code = make_tmdb_request("genre/movie/list", params)
    return JsonResponse(data, safe=False, status=status_code)


@api_view(['GET'])
def fetch_movies(request):
    # /?query=james+bond
    # Capture all parameters from the GET request
    params = request.GET.dict()  # Get all parameters as a dictionary

    # Sanitize parameters
    sanitized_params = sanitize_query_params(params)
    # Check if the 'query' parameter was provided
    if 'query' not in sanitized_params or not sanitized_params['query']:
        return JsonResponse({'error': 'Query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

    data, status_code = make_tmdb_request("search/multi", sanitized_params)
    return JsonResponse(data, safe=False, status=status_code)


@api_view(['GET'])
def tmdb_fetch_movies2(request):
    params = {
        'append_to_response': 'images',
        'language': 'en-US',
        'include_image_language': 'en,null'
    }
    data, status_code = make_tmdb_request("movie/550", params)
    return JsonResponse(data, safe=False, status=status_code)
