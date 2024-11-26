const API_BASE_URL = 'https://capital-cheetah-closely.ngrok-free.app/api';

export const fetchRecommendations = async (userId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/movies/recommended/1`);
    // const response = await fetch(`${API_BASE_URL}/movies/recommended/${userId}`);
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
    const response = await fetch(`${API_BASE_URL}/movies/trending`);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching trending movies:", error);
    throw error;
  }
};

// export const fetchMoviesGenre = async (force = false) => {
//   try {
//     const response = await fetch(`${API_BASE_URL}/movies/genres/?force=${force}`);
//     if (!response.ok) {
//       throw new Error(`HTTP error! Status: ${response.status}`);
//     }
//     return await response.json();
//   } catch (error) {
//     console.error("Error fetching movie genres:", error);
//     throw error;
//   }
// };

export const fetchMoodBased = async (userId) => {
  try {
    // const response = await fetch(`${API_BASE_URL}/movies/mood-based/${userId}`);
    const response = await fetch(`${API_BASE_URL}/movies/mood-based/1`);
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching mood-based movies:", error);
    throw error;
  }
};
