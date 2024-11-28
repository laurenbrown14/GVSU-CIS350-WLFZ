from datetime import datetime, timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
# import datetime
import requests
import re
from movie_suggestion.settings import TMDB_API_KEY, TMDB_API_URL
from .auth_manager import LoginManager
from .models import User, MovieRecommendation, Genre
from .serializers import MovieRecommendationSerializer


# Helper function to sanitize query parameters
def sanitize_query_params(params):
    """Sanitizes query parameters to prevent SQL injection."""
    sanitized_params = {}
    for key, value in params.items():
        if isinstance(value, str):
            sanitized_value = re.sub(r'[^a-zA-Z0-9\s]', '', value)
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
    def get(self, request):

        # from ipdb import set_trace
        # set_trace()

        user = LoginManager().get_user_from_request(request)
        recommendations = MovieRecommendation.get_movies(user=user, movie_type=MovieRecommendation.RECOMMENDATION)
        if not recommendations:
            params = {
                'page': '1',
                'language': 'en-US',
                'sort_by': 'vote_average.desc',
                'include_adult': 'false',
                'include_video': 'false',
                'with_genres': ','.join(map(str, [18, 28])),  # TODO: Get list from logged user.
                'primary_release_date.gte': datetime.now() - timedelta(days=365),
                'vote_average.gte': '9'
            }
            data, status_code = make_tmdb_request("discover/movie", params)
            if status_code == 200:
                new_movies = data['results']
                for movie in new_movies:
                    # Use 'original_title' if 'title' is missing or empty
                    title = movie.get('title') or movie.get('original_title')
                    movie['title'] = title
                MovieRecommendation.add_movies(new_movies, MovieRecommendation.RECOMMENDATION, user)

        movie_recommendation = MovieRecommendation.get_movies(user=user, movie_type=MovieRecommendation.RECOMMENDATION)
        serializer = MovieRecommendationSerializer(movie_recommendation, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# View to get trending movies
class GetTrendingMovies(APIView):
    def get(self, request):
        user = LoginManager().get_user_from_request(request)
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
    def get(self, request):
        user = LoginManager().get_user_from_request(request)
        movies = MovieRecommendation.get_movies(movie_type=MovieRecommendation.TRENDING)
        serializer = MovieRecommendationSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# View to get movie genres and populate the database if necessary
class GetMoviesGenre(APIView):
    def get(self, request):
        user = LoginManager().get_user_from_request(request)
        force = request.GET.get('force', 'false').lower() == 'true'

        if force or not Genre.objects.exists():
            params = {'language': 'en-US'}
            data, status_code = make_tmdb_request("genre/movie/list", params)
            if status_code == 200:
                Genre.populate(data['genres'])
        genres = Genre.objects.all().values('id', 'name')
        return Response(list(genres), status=status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Check if email and password were provided
        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a user with this email exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Authenticate user by checking password
        if user.check_password(password):
            token = LoginManager().generate_token(user)
            return Response({'token': token}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class SignUpView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Validate required fields
        if not email or not password:
            return Response({'error': 'All fields are required: username, email, and password.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already in use.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = User(email=email)
        user.set_password(password)
        user.save()

        # Generate a token for the new user
        token = LoginManager().generate_token(user)

        return Response({'message': 'User created successfully.', 'token': token}, status=status.HTTP_201_CREATED)
