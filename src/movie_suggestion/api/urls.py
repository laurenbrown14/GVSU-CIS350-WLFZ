from django.urls import path
from .views import GetMoviesGenre, GetMovieRecommendation, GetTrendingMovies, GetMoodBasedMovies, LoginView, SignUpView, \
    GetMovieDetails

urlpatterns = [
    path("movies/genres/", GetMoviesGenre.as_view(), name="GetMoviesGenre"),
    path("movies/recommended/", GetMovieRecommendation.as_view(), name="GetMovieRecommendation"),
    path("movies/trending/", GetTrendingMovies.as_view(), name="GetTrendingMovies"),
    path("movies/mood-based/", GetMoodBasedMovies.as_view(), name="GetMoodBasedMovies"),
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("movies/details/<int:movie_id>/", GetMovieDetails.as_view(), name="GetMovieDetails"),
]
