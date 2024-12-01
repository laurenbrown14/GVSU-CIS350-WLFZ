import React, { useState, useEffect } from 'react';
import { SafeAreaView, ActivityIndicator, StyleSheet, ScrollView, View, TextInput, RefreshControl, ImageBackground, StatusBar, TouchableOpacity, Animated, Image } from 'react-native';
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
import MovieDetails from './components/MovieDetails';
import { Ionicons } from '@expo/vector-icons';

const Stack = createStackNavigator();

function Home({ navigation }) {
  const [recommendations, setRecommendations] = useState(null);
  const [trending, setTrending] = useState(null);
  const [moodBased, setMoodBased] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [showSearchBar, setShowSearchBar] = useState(false);
  const searchBarWidth = useState(new Animated.Value(0))[0];

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
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const onRefresh = async () => {
    setRefreshing(true);
    setLoading(true);
    await loadData();
  };

  const toggleSearchBar = () => {
    setShowSearchBar((prev) => !prev);
    Animated.timing(searchBarWidth, {
      toValue: showSearchBar ? 0 : 1,
      duration: 300,
      useNativeDriver: false,
    }).start();
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" backgroundColor="transparent" translucent={true} />
      <ImageBackground source={require('./assets/background.png')} style={styles.backgroundImage} imageStyle={{ opacity: 0.2 }}>
        <StatusBar barStyle="dark-content" backgroundColor="transparent" translucent={true} style={styles.statusBar} />
        <View style={styles.header}>
          <Image source={require('./assets/logo.png')} style={styles.logo} />
          <View style={styles.headerRight}>
            <Animated.View style={[styles.searchBar, { width: searchBarWidth.interpolate({ inputRange: [0, 1], outputRange: ['0%', '75%'] }) }]}>
              {showSearchBar && (
                <TextInput
                  placeholder="Search by title, author or genre"
                  style={styles.searchInput}
                  autoFocus={true}
                />
              )}
            </Animated.View>
            <TouchableOpacity onPress={toggleSearchBar} style={styles.searchIcon}>
              <Ionicons name="search" size={28} color="#8b0000" />
            </TouchableOpacity>
          </View>
        </View>


        {loading && !refreshing ? (
          <ActivityIndicator size="large" color="#0000ff" />
        ) : (
          <ScrollView refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}>
            <Recommendation data={recommendations} />
            <Trending data={trending} />
            <MoodBased data={moodBased} />
          </ScrollView>
        )}
      </ImageBackground>
      <BottomMenu onSearchIconPress={toggleSearchBar} />
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
        <Stack.Screen name="MovieDetails" component={MovieDetails} options={{ headerShown: false }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  backgroundImage: {
    flex: 1,
    resizeMode: 'cover',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 10,
    backgroundColor: '#f5f5f5',
    marginTop: StatusBar.currentHeight,
  },
  logo: {
    width: 100,
    height: 40,
    resizeMode: 'contain',
  },
  headerRight: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusBar: {
    marginRight: 10,
  },
  searchIcon: {
    padding: 5,
  },
  searchBar: {
    overflow: 'hidden',
    backgroundColor: '#f5f5f5',
    paddingHorizontal: 10,
    height: 50,
    justifyContent: 'center',
  },
  searchInput: {
    height: 40,
    backgroundColor: '#fff',
    borderRadius: 8,
    paddingHorizontal: 10,
    borderWidth: 1,
    borderColor: '#ccc',
    color: '#000',
  },
});

export default App;
