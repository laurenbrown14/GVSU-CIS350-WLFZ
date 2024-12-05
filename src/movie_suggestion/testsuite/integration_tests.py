import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
#from django.test import RequestFactory, TestCase


class IntegrationTests(APITestCase): 
    @patch("api.views.make_tmdb_request")
    def test_index(self, mock_tmdb_request):
        """Test the index view."""
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Your API is running!")

    @patch("api.views.make_tmdb_request")
    def test_get_suggestion_list(self, mock_tmdb_request):
        """Test the get_suggestion_list view."""
        # Mock TMDB API response
        mock_tmdb_request.return_value = (
            {"results": [{"id": 1, "title": "Movie A"}, {"id": 2, "title": "Movie B"}]},
            200,
        )
        response = self.client.get(reverse("get_suggestion_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {"results": [{"id": 1, "title": "Movie A"}, {"id": 2, "title": "Movie B"}]},
        )

    @patch("api.views.make_tmdb_request")
    def test_get_movies_genre(self, mock_tmdb_request):
        """Test the get_movies_genre view."""
        # Mock TMDB API response
        mock_tmdb_request.return_value = (
            {"genres": [{"id": 28, "name": "Action"}, {"id": 18, "name": "Drama"}]},
            200,
        )
        response = self.client.get(reverse("get_movies_genre"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {"genres": [{"id": 28, "name": "Action"}, {"id": 18, "name": "Drama"}]},
        )

    @patch("api.views.make_tmdb_request")
    def test_fetch_movies_with_query(self, mock_tmdb_request):
        """Test the fetch_movies view with a valid query."""
        # Mock TMDB API response
        mock_tmdb_request.return_value = (
            {"results": [{"id": 3, "title": "James Bond"}]},
            200,
        )
        response = self.client.get(reverse("fetch_movies") + "?query=james+bond")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content), {"results": [{"id": 3, "title": "James Bond"}]}
        )

    def test_fetch_movies_missing_query(self):
        """Test the fetch_movies view without a query parameter."""
        response = self.client.get(reverse("fetch_movies"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content), {"error": "Query parameter is required."}
        )

    @patch("api.views.make_tmdb_request")
    def test_tmdb_fetch_movies2(self, mock_tmdb_request):
        """Test the tmdb_fetch_movies2 view."""
        # Mock TMDB API response
        mock_tmdb_request.return_value = (
            {"id": 550, "title": "Fight Club", "images": []},
            200,
        )
        response = self.client.get(reverse("tmdb_fetch_movies2"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {"id": 550, "title": "Fight Club", "images": []},
        )
