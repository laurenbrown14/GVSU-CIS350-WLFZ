from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from api.models import User, MovieRecommendation, Genre
from api.auth_manager import LoginManager


class TestSanitizeQueryParams(APITestCase):

    def test_sanitize_query_params(self):
        from api.views import sanitize_query_params

        input_params = {
            "search": "DROP TABLE users;",
            "page": "1",
            "invalid_chars": "test!@#$%^&*()",
        }
        expected_output = {
            "search": "DROP TABLE users",
            "page": "1",
            "invalid_chars": "test",
        }
        self.assertEqual(sanitize_query_params(input_params), expected_output)


class TestMakeTMDBRequest(APITestCase):

    @patch("requests.get")
    def test_make_tmdb_request_success(self, mock_get):
        from api.views import make_tmdb_request

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response

        response, status_code = make_tmdb_request("test_endpoint", {"param": "value"})
        self.assertEqual(status_code, 200)
        self.assertEqual(response, {"results": []})

    @patch("requests.get")
    def test_make_tmdb_request_failure(self, mock_get):
        from api.views import make_tmdb_request

        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        response, status_code = make_tmdb_request("test_endpoint", {"param": "value"})
        self.assertEqual(status_code, 404)
        self.assertIn("error", response)


class TestGetMovieRecommendation(APITestCase):

    @patch("api.views.MovieRecommendation.get_movies")
    @patch("api.views.make_tmdb_request")
    def test_get_movie_recommendation_no_existing_recommendations(self, mock_tmdb_request, mock_get_movies):
        from api.views import GetMovieRecommendation

        mock_get_movies.return_value = []
        mock_tmdb_request.return_value = ({"results": [{"title": "Movie 1"}]}, 200)

        client = APIClient()
        response = client.get("/api/movies/recommendations/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Movie 1")

    @patch("api.views.MovieRecommendation.get_movies")
    def test_get_movie_recommendation_with_existing_recommendations(self, mock_get_movies):
        from api.views import GetMovieRecommendation

        mock_get_movies.return_value = [{"title": "Existing Movie"}]

        client = APIClient()
        response = client.get("/api/movies/recommendations/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Existing Movie")


class TestGetTrendingMovies(APITestCase):

    @patch("api.views.MovieRecommendation.get_movies")
    @patch("api.views.make_tmdb_request")
    def test_get_trending_movies(self, mock_tmdb_request, mock_get_movies):
        mock_get_movies.return_value = []
        mock_tmdb_request.return_value = ({"results": [{"title": "Trending Movie"}]}, 200)

        client = APIClient()
        response = client.get("/api/movies/trending/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Trending Movie")


class TestLoginView(APITestCase):

    @patch("api.views.User.objects.get")
    @patch("api.views.LoginManager.generate_token")
    def test_login_success(self, mock_generate_token, mock_get_user):
        mock_user = MagicMock()
        mock_user.check_password.return_value = True
        mock_get_user.return_value = mock_user
        mock_generate_token.return_value = "test_token"

        client = APIClient()
        response = client.post("/api/auth/login/", {"email": "test@example.com", "password": "password"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["token"], "test_token")

    @patch("api.views.User.objects.get")
    def test_login_invalid_credentials(self, mock_get_user):
        mock_get_user.side_effect = User.DoesNotExist

        client = APIClient()
        response = client.post("/api/auth/login/", {"email": "test@example.com", "password": "password"})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)


class TestSignUpView(APITestCase):

    @patch("api.views.User.objects.filter")
    @patch("api.views.User.save")
    @patch("api.views.LoginManager.generate_token")
    def test_signup_success(self, mock_generate_token, mock_user_save, mock_user_filter):
        mock_user_filter.return_value.exists.return_value = False
        mock_generate_token.return_value = "new_user_token"

        client = APIClient()
        response = client.post(
            "/api/auth/signup/",
            {
                "email": "test@example.com",
                "password": "password",
                "name": "Test User",
                "birthday": "01/01/2000",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["token"], "new_user_token")

    @patch("api.views.User.objects.filter")
    def test_signup_email_exists(self, mock_user_filter):
        mock_user_filter.return_value.exists.return_value = True

        client = APIClient()
        response = client.post(
            "/api/auth/signup/",
            {
                "email": "test@example.com",
                "password": "password",
                "name": "Test User",
                "birthday": "01/01/2000",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)