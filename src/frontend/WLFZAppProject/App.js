import React, { useState, useEffect } from 'react';
import { SafeAreaView, ActivityIndicator, StyleSheet, ScrollView, View, TextInput, RefreshControl, ImageBackground, StatusBar } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import Recommendation from './components/Recommendation';
import Trending from './components/Trending';
import MoodBased from './components/MoodBased';
import BottomMenu from './components/BottomMenu';
import { fetchRecommendations, fetchTrending, fetchMoodBased } from './services/api';
import Login from './components/Login';
import SplashScreen from './components/SplashScreen';
import SignUp from './components/SignUp';


const Stack = createStackNavigator();

function Home() {
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
      <StatusBar barStyle="dark-content" backgroundColor="transparent" translucent={true} />
      <ImageBackground source={require('./assets/background.png')} style={styles.backgroundImage} imageStyle={{ opacity: 0.2 }}>
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

const App = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="SplashScreen">
        <Stack.Screen name="SplashScreen" component={SplashScreen} options={{ headerShown: false }} />
        <Stack.Screen name="Login" component={Login} options={{ headerShown: false }} />
        <Stack.Screen name="SignUp" component={SignUp} options={{ headerShown: false }} />
        <Stack.Screen name="Home" component={Home} options={{ headerShown: false }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  searchBar: {
    padding: 10,
    backgroundColor: '#f5f5f5',
    marginTop: StatusBar.currentHeight, // Adjust for the StatusBar height
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

export default App;
