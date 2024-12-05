import json
import re
from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock
from django.test import RequestFactory, TestCase
from django.http import JsonResponse
from django.urls import reverse
from rest_framework import status
from api.views import (
    index, sanitize_query_params, make_tmdb_request, get_suggestion_list,
    get_movies_genre, fetch_movies, tmdb_fetch_movies2
)


class APITests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_index_view(self):
        request = self.factory.get('/')
        response = index(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Your API is running!")

    def test_sanitize_query_params(self):
        params = {
            'query': 'drop table; --',
            'page': '1',
            'unsafe_key': "<script>alert('xss')</script>"
        }
        sanitized = sanitize_query_params(params)
        self.assertEqual(sanitized['query'], 'drop table')
        self.assertEqual(sanitized['page'], '1')
        self.assertEqual(sanitized['unsafe_key'], 'alertxss')

    @patch('api.views.requests.get')
    def test_make_tmdb_request_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'result': 'success'}
        mock_get.return_value = mock_response

        data, status_code = make_tmdb_request('test/endpoint', {'param': 'value'})
        self.assertEqual(status_code, 200)
        self.assertEqual(data, {'result': 'success'})

    @patch('api.views.requests.get')
    def test_make_tmdb_request_failure(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {'error': 'not found'}
        mock_get.return_value = mock_response

        data, status_code = make_tmdb_request('test/endpoint', {'param': 'value'})
        self.assertEqual(status_code, 404)
        self.assertEqual(data['error'], "Failed to fetch data: 404")

    @patch('api.views.make_tmdb_request')
    def test_get_suggestion_list(self, mock_tmdb_request):
        mock_tmdb_request.return_value = ({"results": []}, 200)

        request = self.factory.get('/api/get_suggestion_list')
        response = get_suggestion_list(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"results": []})

    @patch('api.views.make_tmdb_request')
    def test_get_movies_genre(self, mock_tmdb_request):
        mock_tmdb_request.return_value = ({"genres": []}, 200)

        request = self.factory.get('/api/get_movies_genre')
        response = get_movies_genre(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"genres": []})

    @patch('api.views.make_tmdb_request')
    def test_fetch_movies_valid_query(self, mock_tmdb_request):
        mock_tmdb_request.return_value = ({"results": []}, 200)

        request = self.factory.get('/api/fetch_movies?query=james+bond')
        response = fetch_movies(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"results": []})

    def test_fetch_movies_missing_query(self):
        request = self.factory.get('/api/fetch_movies')
        response = fetch_movies(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['error'], 'Query parameter is required.')

    @patch('api.views.make_tmdb_request')
    def test_tmdb_fetch_movies2(self, mock_tmdb_request):
        mock_tmdb_request.return_value = ({"data": "movie details"}, 200)
        sanitized = sanitize_query_params(mock_tmdb_request.return_value)

        request = self.factory.get('/api/tmdb_fetch_movies2')
        response = tmdb_fetch_movies2(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"data": "movie details"})
        self.assertEqual(sanitized['page'], '1')
        self.assertFalse(sanitized['adult'])

    @patch('api.views.requests.get')
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

    @patch('api.views.requests.get')
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

    @patch('api.views.make_tmdb_request')
    def test_get_suggestion_list(self, mock_tmdb_request):
        mock_tmdb_request.return_value = ({"results": []}, 200)

        response = self.client.get(reverse('get_suggestion_list'))  # Assuming URL pattern is named 'get_suggestion_list'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"results": []})

    @patch('api.views.make_tmdb_request')
    def test_get_movies_genre(self, mock_tmdb_request):
        mock_tmdb_request.return_value = ({"genres": []}, 200)

        response = self.client.get(reverse('get_movies_genre'))  # Assuming URL pattern is named 'get_movies_genre'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"genres": []})

    @patch('api.views.make_tmdb_request')
    def test_fetch_movies_with_query(self, mock_tmdb_request):
        mock_tmdb_request.return_value = ({"results": []}, 200)
        response = self.client.get(reverse('fetch_movies'), {'query': 'james bond'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"results": []})

    def test_fetch_movies_missing_query(self):
        response = self.client.get(reverse('fetch_movies'))  # Missing 'query' parameter
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"error": "Query parameter is required."})

    @patch('api.views.make_tmdb_request')
    def test_tmdb_fetch_movies2(self, mock_tmdb_request):
        mock_tmdb_request.return_value = ({"images": {}}, 200)
        response = self.client.get(reverse('tmdb_fetch_movies2'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"images": {}})
