import React from 'react';
import { View, Text, StyleSheet, Image, Dimensions, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native';


const Recommendation = ({ data }) => {
  const navigation = useNavigation(); // Access the navigation prop using this hook
  if (!data || data.length === 0) {
    return <Text style={styles.noData}>No recommendations available</Text>;
  }

  // Get the first movie from the data
  const movie = data[0];

  return (
    <TouchableOpacity
      onPress={() => navigation.navigate('MovieDetails', {movieId: movie.movieId})} // Navigate to the Movie Details
    >
      <View style={styles.container}>
        <Text style={styles.title}>Our Recommendation</Text>
        <View style={styles.imageContainer}>
          <Image source={{ uri: movie.imageUrl }} style={styles.image} />
          <View style={styles.overlay}>
            <Text style={styles.movieTitle} numberOfLines={1} ellipsizeMode='tail'>{movie.title}</Text>
            <Text style={styles.rating}>
              ⭐ {movie.voteAverage.toFixed(1)} {/* Format to 1 decimal */}
            </Text>
          </View>
        </View>
      </View>
    </TouchableOpacity>
  );
};

const { width: screenWidth } = Dimensions.get('window');

const styles = StyleSheet.create({
  container: {
    padding: 20,
    alignItems: 'flex-start',
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#8b0000',
  },
  imageContainer: {
    width: screenWidth * 0.9,
    borderRadius: 12,
    overflow: 'hidden',
    position: 'relative',
  },
  image: {
    width: '100%',
    height: 200,
  },
  overlay: {
    position: 'absolute',
    bottom: 0,
    width: '100%',
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
    padding: 10,
    alignItems: 'flex-start', // Align items to the start of the overlay
  },
  movieTitle: {
    fontSize: 26,
    fontWeight: 'bold',
    color: '#fff',
  },
  rating: {
    fontSize: 14,
    color: '#FFD700', // Gold color for the star and rating
    marginTop: 5, // Space between title and star
  },
  noData: {
    fontSize: 16,
    color: '#999',
    textAlign: 'center',
  },
});

export default Recommendation;
