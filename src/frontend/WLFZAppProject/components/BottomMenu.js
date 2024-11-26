import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons, FontAwesome, MaterialIcons } from '@expo/vector-icons';

const BottomMenu = () => {
  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.menuItem}>
        <FontAwesome name="smile-o" size={30} color="#8b0000" style={styles.icon} />
        <Text style={styles.label}>Moody</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.menuItem}>
        <Ionicons name="search" size={30} color="#8b0000" style={styles.icon} />
        <Text style={styles.label}>Search</Text>
      </TouchableOpacity>
      <TouchableOpacity style={[styles.menuItem, styles.home]}>
        <View style={styles.homeIconContainer}>
          <Ionicons name="home" size={30} color="#fff" style={styles.homeIcon} />
          <Text style={styles.homeLabel}>Home</Text>
        </View>
      </TouchableOpacity>
      <TouchableOpacity style={styles.menuItem}>
        <MaterialIcons name="library-add" size={30} color="#8b0000" style={styles.icon} />
        <Text style={styles.label}>My Stuff</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.menuItem}>
        <FontAwesome name="user-circle" size={30} color="#8b0000" style={styles.profileIcon} />
        <Text style={styles.label}>Profile</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingVertical: 15,
    borderTopWidth: 1,
    borderTopColor: '#ccc',
    backgroundColor: '#f0f0f0',
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    elevation: 10, // Ensure the bottom menu stays above other elements
    zIndex: 10,
  },
  menuItem: {
    alignItems: 'center',
  },
  icon: {
    marginBottom: 5,
  },
  homeIconContainer: {
    backgroundColor: '#8b0000',
    borderRadius: 15,
    paddingTop: 40,
    paddingBottom: 30,
    paddingLeft: 25,
    paddingRight: 25,
    position: 'absolute',
    bottom: -30,
  },
  homeLabel: {
    fontSize: 12,
    color: '#ffffff',
    marginTop: 5,
    fontWeight: 'bold',
  },
  label: {
    fontSize: 12,
    color: '#8b0000',
    marginTop: 5,
  },
  profileIcon: {
    marginBottom: 5,
  },
});

export default BottomMenu;
