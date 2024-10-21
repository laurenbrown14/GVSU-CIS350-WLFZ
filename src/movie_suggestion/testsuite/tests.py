from django.test import TestCase
from rest_framework.test import APIClient


class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_fetch_movies_by_id(self):
        response = self.client.get('/api/movies/?i=tt3896198')
        self.assertEqual(response.status_code, 200)

    def test_title_in_json_return(self):
        response = self.client.get('/api/movies/?i=tt3896198')
        self.assertIn('Title', response.data)