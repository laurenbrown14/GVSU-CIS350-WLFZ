from django.urls import path
from . import views

urlpatterns = [
        path("", views.index, name="index"),
        # path("movies/", views.fetch_movies, name="fetch_movies"),
        path("movies/", views.fetch_movies, name="fetch_movies"),
        path("movies/genre/", views.get_movies_genre, name="get_movies_genre"),
        path("movies/suggestion/", views.get_suggestion_list, name="get_suggestion_list"),

        # path('api/process/', views.process_data, name='process_data'),
        # path('api/simple/', views.simple_get, name='simple_get'),
]