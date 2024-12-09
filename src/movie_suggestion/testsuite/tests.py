from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from datetime import datetime, timedelta
from unittest.mock import patch
from api.models import User, MovieRecommendation, Genre


class IntegrationTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="testuser@example.com",
            password="password123",
            name="Test User",
            birthday=datetime.strptime("01/01/1990", "%m/%d/%Y"),
        )
        cls.api_client = APIClient()

    def setUp(self):
        self.api_client.force_authenticate(user=self.user)

    def test_get_movie_recommendations_no_existing_recommendations(self):
        """Test retrieving recommendations when none exist in the database."""
        with patch("api.views.make_tmdb_request") as mock_tmdb_request:
            mock_tmdb_request.return_value = ({
                "results": [
                    {"title": "Test Movie 1", "id": 1},
                    {"title": "Test Movie 2", "id": 2},
                ]
            }, 200)

            url = reverse("get_movie_recommendations")
            response = self.api_client.get(url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 2)
            self.assertEqual(response.data[0]["title"], "Test Movie 1")

    def test_get_trending_movies(self):
        """Test retrieving trending movies."""
        # Preload some trending movies
        MovieRecommendation.objects.create(
            title="Trending Movie 1",
            movie_type=MovieRecommendation.TRENDING,
            user=self.user,
        )
        MovieRecommendation.objects.create(
            title="Trending Movie 2",
            movie_type=MovieRecommendation.TRENDING,
            user=self.user,
        )

        url = reverse("get_trending_movies")
        response = self.api_client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], "Trending Movie 1")

    def test_get_movie_genres(self):
        """Test retrieving movie genres."""
        Genre.objects.create(id=1, name="Action")
        Genre.objects.create(id=2, name="Comedy")

        url = reverse("get_movie_genres")
        response = self.api_client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["name"], "Action")

    def test_login(self):
        """Test the login endpoint."""
        url = reverse("login")
        response = self.api_client.post(
            url, {"email": self.user.email, "password": "password123"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_signup(self):
        """Test the signup endpoint."""
        url = reverse("signup")
        response = self.api_client.post(
            url,
            {
                "email": "newuser@example.com",
                "password": "password123",
                "name": "New User",
                "birthday": "01/01/2000",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)

    def test_get_movie_details(self):
        """Test retrieving details for a specific movie."""
        with patch("api.views.make_tmdb_request") as mock_tmdb_request:
            # Mock the TMDB API responses
            mock_tmdb_request.side_effect = [
                ({
                    "title": "Test Movie",
                    "genres": [{"name": "Action"}],
                    "vote_average": 8.5,
                    "overview": "A test movie.",
                    "poster_path": "/test.jpg",
                    "release_date": "2024-01-01",
                    "id": 1,
                }, 200),
                ({
                    "cast": [{"name": "Actor 1", "known_for_department": "Acting"}],
                    "crew": [{"name": "Director 1", "department": "Directing", "job": "Director"}],
                }, 200),
                ({
                    "results": [
                        {"title": "Similar Movie 1", "poster_path": "/similar.jpg", "id": 2},
                    ],
                }, 200),
            ]

            url = reverse("get_movie_details", args=[1])
            response = self.api_client.get(url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["title"], "Test Movie")
            self.assertEqual(response.data["genres"], ["Action"])
            self.assertEqual(response.data["stars"], ["Actor 1"])
            self.assertEqual(response.data["director"], "Director 1")
            self.assertEqual(response.data["more_like_this"][0]["title"], "Similar Movie 1")

    def test_invalid_movie_details(self):
        """Test retrieving details for an invalid movie ID."""
        with patch("api.views.make_tmdb_request") as mock_tmdb_request:
            mock_tmdb_request.return_value = ({"error": "Not Found"}, 404)

            url = reverse("get_movie_details", args=[9999])
            response = self.api_client.get(url)

            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            self.assertIn("error", response.data)