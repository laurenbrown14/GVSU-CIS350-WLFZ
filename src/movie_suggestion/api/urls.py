from django.urls import path
from .views import GetMoviesGenre, GetMovieRecommendation, GetTrendingMovies, GetMoodBasedMovies

urlpatterns = [
    path("movies/genres/", GetMoviesGenre.as_view(), name="GetMoviesGenre"),
    path("movies/recommended/<int:user_id>/", GetMovieRecommendation.as_view(), name="GetMovieRecommendation"),
    path("movies/trending/", GetTrendingMovies.as_view(), name="GetTrendingMovies"),
    path("movies/mood-based/<int:user_id>/", GetMoodBasedMovies.as_view(), name="GetMoodBasedMovies"),
]
