import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Image, Alert, ImageBackground, TouchableWithoutFeedback, Keyboard } from 'react-native';
import { login } from '../services/api';

const Login = ({ navigation }) => {
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');

	const handleLogin = async () => {
		try {
			const response = await login(email, password);
			if (response.token) {
				navigation.navigate('Home');
			}
		} catch (error) {
			Alert.alert('Login Failed', 'Invalid email or password.');
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
						<Text style={styles.title}>Login</Text>
						<TouchableOpacity onPress={() => navigation.navigate('SignUp')}>
							<Text style={styles.signupText}>Don't have an account? <Text style={styles.signupLink}>Sign Up</Text></Text>
						</TouchableOpacity>
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
						<View style={styles.optionsContainer}>
							<TouchableOpacity>
								<Text style={styles.forgotPasswordLink}>Forgot Password?</Text>
							</TouchableOpacity>
						</View>
						<TouchableOpacity style={styles.loginButton} onPress={handleLogin}>
							<Text style={styles.loginButtonText}>Log In</Text>
						</TouchableOpacity>
						<Text style={styles.orText}>Or</Text>
						<TouchableOpacity style={styles.socialButton}>
							<Text style={styles.socialButtonText}>Continue with Google</Text>
						</TouchableOpacity>
						<TouchableOpacity style={styles.socialButton}>
							<Text style={styles.socialButtonText}>Continue with Facebook</Text>
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
		width: 150,
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
	optionsContainer: {
		width: '100%',
		flexDirection: 'row',
		justifyContent: 'space-between',
		marginBottom: 20,
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
	forgotPasswordLink: {
		color: '#8b0000',
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
	orText: {
		color: '#999',
		marginBottom: 20,
		textAlign: 'center',
	},
	socialButton: {
		width: '100%',
		height: 50,
		borderColor: '#ccc',
		borderWidth: 1,
		justifyContent: 'center',
		alignItems: 'center',
		borderRadius: 8,
		marginBottom: 15,
	},
	socialButtonText: {
		fontSize: 16,
		color: '#000',
	},
});

export default Login;
