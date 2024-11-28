from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from api.models import User


class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # self.user = User.objects.create(name="Test User", email="testuser@example.com", birthday="1990-01-01",
        #                                 avatar="", password="testpassword")

    def test_get_movie_recommendation(self):
        url = reverse('GetMovieRecommendation', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_trending_movies(self):
        url = reverse('GetTrendingMovies')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_mood_based_movies(self):
        url = reverse('GetMoodBasedMovies', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_movies_genre(self):
        url = reverse('GetMoviesGenre')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
