import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Image, Alert, ImageBackground, TouchableWithoutFeedback, Keyboard, ActivityIndicator } from 'react-native';
import { signUp } from '../services/api';
import MaskInput from 'react-native-mask-input';

const SignUp = ({ navigation }) => {
  const [name, setName] = useState('');
  const [birthday, setBirthday] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSignUp = async () => {
    // Input Validation
    if (!name || !birthday || !email || !password) {
      Alert.alert('Invalid Input', 'Please fill in all fields.');
      return;
    }
    if (!/\S+@\S+\.\S+/.test(email)) {
      Alert.alert('Invalid Email', 'Please enter a valid email address.');
      return;
    }
    if (!/\d{2}\/\d{2}\/\d{4}/.test(birthday)) {
      Alert.alert('Invalid Date', 'Please enter a valid date in MM/DD/YYYY format.');
      return;
    }

    setLoading(true);
    try {
      const response = await signUp(email, password, name, birthday);
      if (response.token) {
        navigation.navigate('Home');
      }
    } catch (error) {
      Alert.alert('Sign Up Failed', error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <TouchableWithoutFeedback onPress={Keyboard.dismiss} accessible={false}>
      <ImageBackground source={require('../assets/background.png')} style={styles.backgroundImage} imageStyle={{ opacity: 0.3 }}>
        <View style={styles.logoContainer}>
          <Image source={require('../assets/logo.png')} style={styles.logo} />
        </View>
        <View style={styles.container}>
          <View style={styles.boxContainer}>
            <Text style={styles.title}>Sign Up</Text>
            <TouchableOpacity onPress={() => navigation.navigate('Login')}>
              <Text style={styles.signupText}>Already have an account? <Text style={styles.signupLink}>Log In</Text></Text>
            </TouchableOpacity>
            <Text style={styles.label}>Name</Text>
            <TextInput
              style={styles.input}
              placeholder="Name"
              value={name}
              onChangeText={setName}
            />
            <Text style={styles.label}>Date of Birth</Text>
            <MaskInput
              style={styles.input}
              value={birthday}
              onChangeText={(masked, birthday) => {
                setBirthday(masked);
              }}
              mask={[/\d/, /\d/, '/', /\d/, /\d/, '/', /\d/, /\d/, /\d/, /\d/]}
              placeholder="MM/DD/YYYY"
              keyboardType="numeric"
            />
            <Text style={styles.label}>Email</Text>
            <TextInput
              style={styles.input}
              placeholder="Email"
              value={email}
              onChangeText={setEmail}
              keyboardType="email-address"
            />
            <Text style={styles.label}>Password</Text>
            <TextInput
              style={styles.input}
              placeholder="Password"
              value={password}
              onChangeText={setPassword}
              secureTextEntry
            />
            <TouchableOpacity style={styles.loginButton} onPress={handleSignUp}>
              {loading ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <Text style={styles.loginButtonText}>Sign Up</Text>
              )}
            </TouchableOpacity>
          </View>
        </View>
      </ImageBackground>
    </TouchableWithoutFeedback>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'flex-start',
    alignItems: 'center',
    padding: 20,
  },
  backgroundImage: {
    flex: 1,
    resizeMode: 'cover',
  },
  logoContainer: {
    alignItems: 'center',
    marginTop: 50,
    marginBottom: 10,
  },
  boxContainer: {
    width: '100%',
    maxWidth: 400,
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  logo: {
    width: 250,
    height: 150,
    resizeMode: 'contain',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    color: '#8b0000',
    alignSelf: 'center',
  },
  label: {
    fontSize: 16,
    color: '#333',
    marginBottom: 5,
  },
  input: {
    width: '100%',
    height: 50,
    borderColor: '#ccc',
    borderWidth: 1,
    marginBottom: 15,
    paddingHorizontal: 10,
    borderRadius: 8,
  },
  signupText: {
    color: '#555',
    alignSelf: 'center',
    marginBottom: 20,
  },
  signupLink: {
    color: '#8b0000',
    fontWeight: 'bold',
  },
  loginButton: {
    width: '100%',
    height: 50,
    backgroundColor: '#8b0000',
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 8,
    marginBottom: 20,
  },
  loginButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});

export default SignUp;
