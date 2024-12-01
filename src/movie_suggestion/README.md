# Movie Recommendation API

This README provides an overview and guidelines for the Movie Recommendation API project. This API serves as a backend for suggesting movies to users based on their preferences, trending data, or mood-based criteria. The project uses Python 3.13.0, Django, and Django REST framework to create and manage the API endpoints.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Endpoints](#endpoints)
- [Authentication](#authentication)
- [Middleware](#middleware)
- [Usage](#usage)

## Project Overview
The Movie Recommendation API offers a variety of movie recommendations, including personalized suggestions, trending films, and mood-based options. The API allows users to interact with different types of data from an external movie database (TMDB API), store recommendations in the database, and personalize their movie-watching experience.

## Features
- User authentication using JWT tokens.
- Movie recommendation with an expiration period.
- Trending movie list retrieval.
- User-specific movie recommendations based on genre preferences.
- Secure API with middleware for request validation and rate-limiting.

## Technologies Used
- **Python 3.13.0**
- **Django 5.1.2**
- **Django REST Framework 3.15.2**
- **JWT Authentication**
- **SQLite** (can be changed to any other supported database)
- **TMDB API** for fetching movie information

The `requirements.txt` file contains all the necessary dependencies for the project, such as:
- **Django** for building the backend.
- **Django CORS Headers** for cross-origin requests support.
- **djangorestframework** for creating RESTful APIs.
- **PyJWT** for token-based authentication.
- **requests** for making HTTP requests to external APIs.

## Setup Instructions
Follow these steps to set up the project locally:

### Prerequisites
- Python 3.13.0
- Virtual Environment (optional, but recommended)

### Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd movie-recommendation-api
   ```
2. Create a virtual environment (optional):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the Django project:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser  # Create an admin user to access the admin panel
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Endpoints

### Authentication
- **`POST /api/login/`**: Allows users to log in and get a JWT token.
- **`POST /api/signup/`**: Register a new user.

### Movie Endpoints
- **`GET /api/movies/recommended/`**: Get recommended movies for the authenticated user.
- **`GET /api/movies/trending/`**: Get a list of trending movies.
- **`GET /api/movies/mood-based/`**: Get mood-based movie recommendations for the authenticated user.
- **`GET /api/movies/genres/`**: Retrieve the available genres (populated from the TMDB API).
- **`GET /api/movies/details/<movie_id>/`**: Get detailed information about a specific movie, including cast, director, and related movies.

## Authentication
The API uses JSON Web Tokens (JWT) for authentication. To interact with the secure endpoints, users must include the `Authorization: Bearer <token>` header in their requests.

To obtain a token, use the `/api/login/` endpoint by providing a valid email and password.

## Middleware
Custom authentication middleware is implemented to ensure that each request carries a valid JWT token. This middleware intercepts requests and validates tokens before allowing access to the API views. Requests to `/login/` and `/signup/` are excluded from this validation.

## Usage
- **User Login**: Use `/api/login/` to authenticate and get a token.
- **Header Requirements**: Include the `Authorization` header with the value `Bearer <JWT>` for all subsequent requests.
- **Movie Recommendations**: Use the provided endpoints to fetch recommendations, trending movies, or user mood-based suggestions.

### Example Request
To get trending movies:
```bash
curl -X GET http://localhost:8000/api/movies/trending/ \
  -H "Authorization: Bearer <your_jwt_token>"
```

## Notes
- The middleware currently requires all endpoints to have a valid token. Ensure you log in and obtain a token before making requests.
- Environment-specific variables (such as API keys) are stored in a separate `api_keys.py` file, which should not be committed to version control.
- Custom user model is implemented to handle user-specific preferences and genres.
- The `LoginManager` in `auth_manager.py` handles user authentication, token generation, and validation.
- The project utilizes TMDB API to fetch movie information, genres, and trending movies. Requests are managed using the helper function `make_tmdb_request()`.

## Contributing
Contributions are welcome! Please fork this repository, make changes, and submit a pull request for review.

## License
This project is licensed under the MIT License.

