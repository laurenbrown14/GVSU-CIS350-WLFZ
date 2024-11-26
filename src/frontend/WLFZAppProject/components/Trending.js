import React from 'react';
import { View, Text, Image, StyleSheet } from 'react-native';

const Trending = ({ data }) => {
  if (!data || data.length === 0) {
    return <Text style={styles.noData}>No trending movies available</Text>;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Trending</Text>
      <View style={styles.movieSection}>
        {data.slice(0, 3).map((movie, index) => (
          <View key={index} style={styles.movieCard}>
            <Image source={{ uri: movie.imageUrl }} style={styles.image} />
            <View style={styles.overlay}>
              <Text style={styles.rank}>{index + 1}</Text>
            </View>
            <Text style={styles.movieTitle}>{movie.title}</Text>
            <Text style={styles.rating}>⭐ {movie.voteAverage.toFixed(1)}</Text>
          </View>
        ))}
      </View>
      <View style={styles.movieSection}>
        {data.slice(3, 6).map((movie, index) => (
          <View key={index + 3} style={styles.movieCard}>
            <Image source={{ uri: movie.imageUrl }} style={styles.image} />
            <View style={styles.overlay}>
              <Text style={styles.rank}>{index + 4}</Text>
            </View>
            <Text style={styles.movieTitle}>{movie.title}</Text>
            <Text style={styles.rating}>⭐ {movie.voteAverage.toFixed(1)}</Text>
          </View>
        ))}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 20,
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#8b0000',
  },
  movieSection: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 10,
  },
  movieCard: {
    position: 'relative',
    alignItems: 'center',
    width: 120,
  },
  image: {
    width: 120,
    height: 180,
    borderRadius: 12,
  },
  overlay: {
    position: 'absolute',
    top: 10,
    left: 10,
    backgroundColor: 'rgba(255, 215, 0, 0.9)',
    borderRadius: 50,
    width: 40,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
  },
  rank: {
    fontSize: 35,
    fontWeight: 'bold',
    color: '#fff',
  },
  movieTitle: {
    marginTop: 8,
    fontSize: 16,
    fontWeight: 'bold',
    textAlign: 'center',
    color: '#000',
  },
  rating: {
    fontSize: 14,
    color: '#8b0000',
    marginTop: 4,
  },
  noData: {
    fontSize: 16,
    color: '#999',
    textAlign: 'center',
  },
});

export default Trending;