import React from 'react';
import { View, Text, Image, StyleSheet } from 'react-native';

const MoodBased = ({ data }) => {
  if (!data || data.length === 0) {
    return <Text style={styles.noData}>No mood-based suggestions available</Text>;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Based on Your Mood</Text>
      <View style={styles.movieSection}>
        {data.map((movie, index) => (
          <Image key={index} source={{ uri: movie.image }} style={styles.image} />
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
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#8b0000',
  },
  movieSection: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 10,
  },
  image: {
    width: 100,
    height: 150,
    borderRadius: 12,
  },
  noData: {
    fontSize: 16,
    color: '#999',
    textAlign: 'center',
  },
});

export default MoodBased;
