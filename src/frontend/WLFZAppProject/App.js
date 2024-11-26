import React, { useState, useEffect } from 'react';
import { SafeAreaView, ActivityIndicator, StyleSheet, ScrollView, View, TextInput, RefreshControl, ImageBackground } from 'react-native';
import Recommendation from './components/Recommendation';
import Trending from './components/Trending';
import MoodBased from './components/MoodBased';
import BottomMenu from './components/BottomMenu';
import { fetchRecommendations, fetchTrending, fetchMoodBased } from './services/api';

export default function App() {
  const [recommendations, setRecommendations] = useState(null);
  const [trending, setTrending] = useState(null);
  const [moodBased, setMoodBased] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const loadData = async () => {
    try {
      const [recommendationData, trendingData, moodBasedData] = await Promise.all([
        fetchRecommendations(),
        fetchTrending(),
        fetchMoodBased(),
      ]);
      setRecommendations(recommendationData);
      setTrending(trendingData);
      setMoodBased(moodBasedData);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
      setRefreshing(false); // Stop refreshing animation
    }
  };

  // Initial data loading
  useEffect(() => {
    loadData();
  }, []);

  // Pull-to-Refresh function
  const onRefresh = async () => {
    setRefreshing(true);
    setLoading(true); // Optional: Show loading spinner
    await loadData();
  };

  return (
    <SafeAreaView style={styles.container}>
      <ImageBackground source={require('./assets/background.png')} style={styles.backgroundImage} imageStyle={{ opacity: 0.3 }}>

        <View style={styles.searchBar}>
          <TextInput placeholder="Search by title, author or genre" style={styles.searchInput} />
        </View>
        {loading && !refreshing ? (
          <ActivityIndicator size="large" color="#0000ff" />
        ) : (
          <ScrollView
            refreshControl={
              <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
            }
          >
            <Recommendation data={recommendations} />
            <Trending data={trending} />
            <MoodBased data={moodBased} />
          </ScrollView>
        )}
      </ImageBackground>
        <BottomMenu />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  searchBar: {
    padding: 10,
    backgroundColor: '#f5f5f5',
  },
  searchInput: {
    height: 40,
    backgroundColor: '#fff',
    borderRadius: 8,
    paddingHorizontal: 10,
    borderWidth: 1,
    borderColor: '#ccc',
  },
  backgroundImage: {
    flex: 1,
    resizeMode: 'cover',
  },
});
