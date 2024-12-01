# WLFZ TV - Movie and TV Series Suggestion App

WLFZ TV is a mobile application that provides personalized recommendations for movies and TV series based on user preferences and moods. The app features trending movies, mood-based suggestions, and other tailored content, utilizing data fetched from an API backend. Built using React Native and Expo, WLFZ TV aims to enhance user engagement with personalized movie experiences.

## Features

- **User Authentication**: Sign up and login functionalities using secure token-based authentication.
- **Recommendations**: Personalized movie and TV series recommendations.
- **Trending Content**: Get the latest trending movies updated in real-time.
- **Mood-Based Suggestions**: Discover movies and series based on your current mood.
- **Interactive Search**: Search movies and TV shows by title, author, or genre.
- **Smooth Navigation**: Fluid navigation between different screens with React Navigation.

## Project Structure

The main files of the project include:

- **App.js**: The entry point of the application, sets up navigation, handles loading and refreshing of data, and manages the animated search bar.
- **components/**: This folder contains the following components:
  - **Recommendation.js**: Displays personalized movie recommendations.
  - **Trending.js**: Displays a list of trending movies.
  - **MoodBased.js**: Shows movie suggestions based on the user's current mood.
  - **BottomMenu.js**: Provides navigation controls for the bottom of the app.
  - **Login.js**, **SignUp.js**, **SplashScreen.js**: Handle user authentication and onboarding.
  - **MovieDetails.js**: Displays detailed information for a selected movie or TV series.
- **services/api.js**: Manages API requests for data like recommendations, trending content, mood-based suggestions, and user authentication.

## Prerequisites

- **Node.js** (>=14.x recommended)
- **Expo CLI** (>=5.0.0)
- **React Native Environment**
- **Ngrok** (optional, for tunneling API during development)

## Installation

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

## Available Scripts

In the project directory, you can run:

- **`npm start`**: Starts the app in Expo Go.
- **`npm run android`**: Builds and runs the app on an Android emulator.
- **`npm run ios`**: Builds and runs the app on an iOS simulator (macOS only).
- **`npm run web`**: Runs the app in a web browser.

## API Endpoints

The API is used to fetch various data for the app, including:

- **`/login/`**: User authentication.
- **`/signup/`**: User registration.
- **`/movies/recommended/`**: Fetch personalized recommendations.
- **`/movies/trending/`**: Fetch trending movies.
- **`/movies/mood-based/`**: Fetch mood-based movie suggestions.
- **`/movies/details/:movieId/`**: Fetch movie details by ID.

## Dependencies

Key dependencies used in the project are:

- **React Native**: Provides the framework for building the mobile app.
- **React Navigation**: Used for routing and navigation within the app.
- **Expo**: Helps in the development workflow for React Native apps.
- **Moment.js**: Utility for date manipulation.
- **React Native AsyncStorage**: Handles secure token storage for authentication.
- **react-native-mask-input**: Used for formatting input fields such as the date of birth.

For a full list of dependencies, check out the `package.json` file.

## How to Use

1. **Sign Up/Login**: Create an account or log in to access recommendations.
2. **Explore Movies**: Browse trending, recommended, and mood-based movies.
3. **Search**: Use the search feature to look for specific movies or TV shows.
4. **View Details**: Tap on a movie to view detailed information.

## Screenshots

![Splash Screen](./assets/screenshots/splashscreen.png)
![Login Screen](./assets/screenshots/login.png)
![Sign Up Screen](./assets/screenshots/signup.png)
![Home Screen](./assets/screenshots/home.png)
![Detail Screen](./assets/screenshots/detail.png)

## Future Improvements

- **Offline Support**: Implement local caching for offline movie viewing.
- **Enhanced Recommendations**: Improve algorithms for better personalization.
- **User Profiles**: Add user profile management and customization features.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests.

## License

This project is licensed under the MIT License.


