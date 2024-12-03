# WLFZ

The conecpt of out project is to allow users to input certain infomartion based on their interests in different movies and we will output some ideas that they could watch. We would also give them them information on the movie, a sneak peak of it, and also check where it can be watched. The purpsoe of our project is to allow you to find something to watch without having to worry about endless scrolling. We can instead give you ideas that you will like.  

## Team Members and Roles

- [Lauren Brown](https://github.com/laurenbrown14/CIS350-HW2-Brown) - Front End Developer and GitHub Manager
* [William Almado](https://github.com/almado/CIS350-HW2-ALMADO) - Back End Developer
* [Fortune Dessin](https://github.com/FDessin/CIS350-HW2-Dessin) - Team Leader and Front End Developer
- [Zander Barth](https://github.com/ZanTheZan/CIS350-HW2-Barth.git) - Back End Developer and Tester

## Prerequisites

### Frontend
- **Node.js** (>=14.x recommended)
- **Expo CLI** (>=5.0.0)
- **React Native Environment**
- **Ngrok** (optional, for tunneling API during development)

### Backend
- **Python** 3.13.0
- **Virtual Environment** (optional, but recommended)

## Run Instructions

## Frontend

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/username/wlfz_tv.git
   cd wlfz_tv
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npx expo start
   ```

### Available Scripts

In the project directory, you can run:

- **`npm start`**: Starts the app in Expo Go.
- **`npm run android`**: Builds and runs the app on an Android emulator.
- **`npm run ios`**: Builds and runs the app on an iOS simulator (macOS only).
- **`npm run web`**: Runs the app in a web browser.

### API Endpoints

The API is used to fetch various data for the app, including:

- **`/login/`**: User authentication.
- **`/signup/`**: User registration.
- **`/movies/recommended/`**: Fetch personalized recommendations.
- **`/movies/trending/`**: Fetch trending movies.
- **`/movies/mood-based/`**: Fetch mood-based movie suggestions.
- **`/movies/details/:movieId/`**: Fetch movie details by ID.

### Dependencies

Key dependencies used in the project are:

- **React Native**: Provides the framework for building the mobile app.
- **React Navigation**: Used for routing and navigation within the app.
- **Expo**: Helps in the development workflow for React Native apps.
- **Moment.js**: Utility for date manipulation.
- **React Native AsyncStorage**: Handles secure token storage for authentication.
- **react-native-mask-input**: Used for formatting input fields such as the date of birth.

For a full list of dependencies, check out the `package.json` file.

### How to Use

1. **Sign Up/Login**: Create an account or log in to access recommendations.
2. **Explore Movies**: Browse trending, recommended, and mood-based movies.
3. **Search**: Use the search feature to look for specific movies or TV shows.
4. **View Details**: Tap on a movie to view detailed information.

## Backend

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

### Endpoints

### Authentication
- **`POST /api/login/`**: Allows users to log in and get a JWT token.
- **`POST /api/signup/`**: Register a new user.

### Movie Endpoints
- **`GET /api/movies/recommended/`**: Get recommended movies for the authenticated user.
- **`GET /api/movies/trending/`**: Get a list of trending movies.
- **`GET /api/movies/mood-based/`**: Get mood-based movie recommendations for the authenticated user.
- **`GET /api/movies/genres/`**: Retrieve the available genres (populated from the TMDB API).
- **`GET /api/movies/details/<movie_id>/`**: Get detailed information about a specific movie, including cast, director, and related movies.

### Authentication
The API uses JSON Web Tokens (JWT) for authentication. To interact with the secure endpoints, users must include the `Authorization: Bearer <token>` header in their requests.

To obtain a token, use the `/api/login/` endpoint by providing a valid email and password.

### Middleware
Custom authentication middleware is implemented to ensure that each request carries a valid JWT token. This middleware intercepts requests and validates tokens before allowing access to the API views. Requests to `/login/` and `/signup/` are excluded from this validation.

