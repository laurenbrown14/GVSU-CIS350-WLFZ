from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import datetime
import requests
import re
from movie_suggestion.settings import TMDB_API_KEY, TMDB_API_URL
from .models import User, MovieRecommendation, Genre
from .serializers import MovieRecommendationSerializer


# Helper function to sanitize query parameters
def sanitize_query_params(params):
    """Sanitizes query parameters to prevent SQL injection."""
    sanitized_params = {}
    for key, value in params.items():
        if isinstance(value, str):
            sanitized_value = re.sub(r'[^a-zA-Z0-9\\s]', '', value)
            sanitized_params[key] = sanitized_value.strip()
        else:
            sanitized_params[key] = value
    return sanitized_params


# Helper function to make requests to the TMDB API
def make_tmdb_request(endpoint, params=None):
    """Helper function to make requests to the TMDB API."""
    url = f"{TMDB_API_URL}/{endpoint}"
    headers = {
        "accept": "application/json",
        "Authorization": TMDB_API_KEY
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json(), 200
    else:
        return {'error': f"Failed to fetch data: {response.status_code}"}, response.status_code


# View to get a movie recommendation for a specific user
class GetMovieRecommendation(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        recommendations = MovieRecommendation.get_movies(user=user, movie_type=MovieRecommendation.RECOMMENDATION)
        serializer = MovieRecommendationSerializer(recommendations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# View to get trending movies
class GetTrendingMovies(APIView):
    def get(self, request):
        # Get existing trending movies from the database
        trending_movies = MovieRecommendation.get_movies(movie_type=MovieRecommendation.TRENDING)
        valid_movies_count = trending_movies.count()

        # If less than 6 trending movies, fetch more from the API
        if valid_movies_count < 6:
            movies_needed = 6 - valid_movies_count
            params = {
                'page': '1',
                'language': 'en-US',
                'sort_by': 'popularity.desc',
                'include_adult': 'false',
                'include_video': 'false'
            }
            data, status_code = make_tmdb_request("trending/movie/day", params)
            if status_code == 200:
                new_movies = data['results'][:movies_needed]
                for movie in new_movies:
                    # Use 'original_title' if 'title' is missing or empty
                    title = movie.get('title') or movie.get('original_title')
                    movie['title'] = title
                MovieRecommendation.add_movies(new_movies, MovieRecommendation.TRENDING)

        # Retrieve updated list of trending movies
        trending_movies = MovieRecommendation.get_movies(movie_type=MovieRecommendation.TRENDING)[:6]
        serializer = MovieRecommendationSerializer(trending_movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# View to get movies by mood or user preferences
class GetMoodBasedMovies(APIView):
    def get(self, request, user_id):
        movies = MovieRecommendation.get_movies(movie_type=MovieRecommendation.TRENDING)
        serializer = MovieRecommendationSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# View to get movie genres and populate the database if necessary
class GetMoviesGenre(APIView):
    def get(self, request):
        force = request.GET.get('force', 'false').lower() == 'true'

        if force or not Genre.objects.exists():
            params = {'language': 'en-US'}
            data, status_code = make_tmdb_request("genre/movie/list", params)
            if status_code == 200:
                Genre.populate(data['genres'])
        genres = Genre.objects.all().values('id', 'name')
        return Response(list(genres), status=status.HTTP_200_OK)
