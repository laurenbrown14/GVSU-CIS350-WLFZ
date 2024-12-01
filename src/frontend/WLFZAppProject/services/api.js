import AsyncStorage from '@react-native-async-storage/async-storage';

const API_BASE_URL = 'https://capital-cheetah-closely.ngrok-free.app/api';

export const fetchRecommendations = async (userId) => {
  try {
    const token = await AsyncStorage.getItem('token'); // Retrieve the token from AsyncStorage
    if (!token) {
      throw new Error('No token found');
    }
    const response = await fetch(`${API_BASE_URL}/movies/recommended/`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`, // Add the token in the Authorization header
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching recommendations:", error);
    throw error;
  }
};

export const fetchTrending = async () => {
  try {
    const token = await AsyncStorage.getItem('token'); // Retrieve the token from AsyncStorage
    if (!token) {
      throw new Error('No token found');
    }
    const response = await fetch(`${API_BASE_URL}/movies/trending/`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching trending movies:", error);
    throw error;
  }
};

export const fetchMoodBased = async (userId) => {
  try {
    const token = await AsyncStorage.getItem('token'); // Retrieve the token from AsyncStorage
    if (!token) {
      throw new Error('No token found');
    }
    const response = await fetch(`${API_BASE_URL}/movies/mood-based/`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching mood-based movies:", error);
    throw error;
  }
};


export const login = async (email, password) => {
  try {
    const response = await fetch(`${API_BASE_URL}/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    await AsyncStorage.setItem('token', data.token); // Save the token for later use

    return data;
  } catch (error) {
    console.error('Error logging in:', error);
    throw error;
  }
};


export const signUp = async (email, password, name, birthday) => {
  try {

    const response = await fetch(`${API_BASE_URL}/signup/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({email, password, name, birthday}),
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    await AsyncStorage.setItem('token', data.token); // Save the token for later use

    return data;
  } catch (error) {
    console.error('Error signing up:', error);
    throw error;
  }
};

export const fetchMovieDetails = async (movieId) => {
  try {
    const token = await AsyncStorage.getItem('token'); // Retrieve the token from AsyncStorage
    if (!token) {
      throw new Error('No token found');
    }

    const response = await fetch(`${API_BASE_URL}/movies/details/${movieId}/`, {
      method: 'GET',
      headers: {
        'accept': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching movie details:', error);
    throw error;
  }
};



