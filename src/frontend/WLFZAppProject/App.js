// import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { StyleSheet, SafeAreaView, StatusBar } from 'react-native';
import { WebView } from 'react-native-webview';

export default function App() {
  return (
    <SafeAreaView style={styles.container}>
      <StatusBar 
        barStyle="default" // light-contentor 'dark-content' depending on your color scheme
        backgroundColor="#000000" // Change this to your desired color
      />
      <WebView 
        originWhitelist={['*']}
        source={require('./assets/index.html')} // Update with your HTML file
        style={styles.webview} 
        scalesPageToFit={false} // Disable page scaling
      />
      <StatusBar style="auto" />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  webview: {
    flex: 1,
  },
});
