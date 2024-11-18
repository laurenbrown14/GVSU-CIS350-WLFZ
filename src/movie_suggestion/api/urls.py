from django.urls import path
from . import views

urlpatterns = [
        path("", views.index, name="index"),
        # path("movies/", views.fetch_movies, name="fetch_movies"),
        path("movies/", views.fetch_movies, name="fetch_movies"),
        path("movies/genre/", views.get_movies_genre, name="get_movies_genre"),
        path("movies/recommended/", views.get_recommended_movie, name="get_recommended_movie"),
        path("movies/trending/", views.get_trending_movie, name="get_trending_movie"),
        path("movies/mood-based/", views.get_mood_based_movie, name="get_mood_based_movie"),

        # path('api/process/', views.process_data, name='process_data'),
        # path('api/simple/', views.simple_get, name='simple_get'),
]