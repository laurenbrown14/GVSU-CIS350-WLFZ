from django.test import TestCase, Client
from rest_framework.test import APIClient

from unittest.mock import patch, MagicMock
from django.urls import reverse

from api.views import (
    sanitize_query_params,
    make_tmdb_request,
    get_suggestion_list,
    get_movies_genre,
    fetch_movies,
    tmdb_fetch_movies2
)

from rest_framework import status
import json

class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_index_view(self):
        """Test if the index view returns the correct message."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Your API is running!")

    def test_fetch_movies(self):
        response = self.client.get('/api/movies/?query=james+bond')
        self.assertEqual(response.status_code, 200)

    # def test_title_in_json_return(self):
    #     response = self.client.get('/api/movies/??query=james+bond')
    #     self.assertIn('Title', response.data)

    def test_get_movies_genre(self):
        """Test if the genre list API returns a valid response."""
        response = self.client.get('/api/genres/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('genres', response.json())

    def test_get_suggestion_list(self):
        """Test if the suggestion list API returns a valid response."""
        response = self.client.get('/api/suggestions/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.json())

    def test_fetch_movies_no_query_param(self):
        """Test if the fetch movies API returns an error when no query parameter is provided."""
        response = self.client.get('/api/fetch-movies/')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Query parameter is required.'})

    def test_fetch_movies_with_query_param(self):
        """Test if the fetch movies API works when a query parameter is provided."""
        response = self.client.get('/api/fetch-movies/', {'query': 'james bond'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.json())



class UnitTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.tmdb_api_key = "mock_api_key"
        self.tmdb_api_url = "https://api.themoviedb.org/3"

    def test_index(self):
        response = self.client.get(reverse('index'))  # Assuming URL pattern is named 'index'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Your API is running!")

    def test_sanitize_query_params(self):

        params = {
            'query': 'james+bond<script>',
            'page': ' 1 ',
            'adult': False
        }
        sanitized = sanitize_query_params(params)
        self.assertEqual(sanitized['query'], 'jamesbond')
        self.assertEqual(sanitized['page'], '1')
        self.assertFalse(sanitized['adult'])

    @patch('movie_suggestion.views.requests.get')
    def test_make_tmdb_request_success(self, mock_get):

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response

        endpoint = "discover/movie"
        params = {'language': 'en-US'}
        data, status_code = make_tmdb_request(endpoint, params)

        self.assertEqual(status_code, 200)
        self.assertEqual(data, {"results": []})
        mock_get.assert_called_once_with(
            f"{self.tmdb_api_url}/{endpoint}",
            headers={
                "accept": "application/json",
                "Authorization": self.tmdb_api_key
            },
            params=params
        )

    @patch('movie_suggestion.views.requests.get')
    def test_make_tmdb_request_failure(self, mock_get):
        from api.views import make_tmdb_request

        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        endpoint = "discover/movie"
        params = {'language': 'en-US'}
        data, status_code = make_tmdb_request(endpoint, params)

        self.assertEqual(status_code, 404)
        self.assertIn('error', data)

    @patch('movie_suggestion.views.make_tmdb_request')
    def test_get_suggestion_list(self, mock_tmdb_request):
        mock_tmdb_request.return_value = ({"results": []}, 200)

        response = self.client.get(reverse('get_suggestion_list'))  # Assuming URL pattern is named 'get_suggestion_list'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"results": []})

    @patch('movie_suggestion.views.make_tmdb_request')
    def test_get_movies_genre(self, mock_tmdb_request):
        mock_tmdb_request.return_value = ({"genres": []}, 200)

        response = self.client.get(reverse('get_movies_genre'))  # Assuming URL pattern is named 'get_movies_genre'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"genres": []})

    @patch('movie_suggestion.views.make_tmdb_request')
    def test_fetch_movies_with_query(self, mock_tmdb_request):
        mock_tmdb_request.return_value = ({"results": []}, 200)
        response = self.client.get(reverse('fetch_movies'), {'query': 'james bond'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"results": []})

    def test_fetch_movies_missing_query(self):
        response = self.client.get(reverse('fetch_movies'))  # Missing 'query' parameter
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "Query parameter is required."})

    @patch('movie_suggestion.views.make_tmdb_request')
    def test_tmdb_fetch_movies2(self, mock_tmdb_request):
        mock_tmdb_request.return_value = ({"images": {}}, 200)
        response = self.client.get(reverse('tmdb_fetch_movies2'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"images": {}})