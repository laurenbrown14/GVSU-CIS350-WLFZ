from django.test import TestCase
from rest_framework.test import APIClient


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
    pass