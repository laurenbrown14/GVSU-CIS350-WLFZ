import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, Image, ScrollView, ActivityIndicator, TouchableOpacity } from 'react-native';
import { fetchMovieDetails } from '../services/api';
import { Ionicons } from '@expo/vector-icons';  // Assuming you're using Expo, to add icons
import moment from 'moment';


const MovieDetails = ({ route, navigation }) => {
	const { movieId } = route.params;
	const [movieDetails, setMovieDetails] = useState(null);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		const loadMovieDetails = async () => {
			try {
				const data = await fetchMovieDetails(movieId);
				setMovieDetails(data);
			} catch (error) {
				console.error('Error loading movie details:', error);
			} finally {
				setLoading(false);
			}
		};
		loadMovieDetails();
	}, [movieId]);

	if (loading) {
		return <ActivityIndicator size="large" color="#8b0000" style={styles.loading} />;
	}

	if (!movieDetails) {
		return <Text style={styles.errorText}>Failed to load movie details.</Text>;
	}

	return (
		<ScrollView style={styles.container}>
			<View style={styles.topSection}>
				{/* Background Image */}
				<Image source={{ uri: movieDetails.image }} style={styles.backgroundImage} />

				{/* Back Button */}

				<TouchableOpacity onPress={() => navigation.push('Home')} style={styles.backButton}>
					<Ionicons name="close-sharp" size={28} color="#fff" />
				</TouchableOpacity>
			</View>

			{/* Movie Details */}
			<View style={styles.detailsContainer}>

				{/* Poster Image and Movie Details */}
				<View style={styles.posterContainer}>
					<Image source={{ uri: movieDetails.image }} style={styles.poster} />
					<View style={styles.movieInfo}>
						<Text style={styles.title}>{movieDetails.title}</Text>
						<View style={styles.ratingContainer}>
							<Ionicons name="star" size={16} color="#FFD700" />
							<Text style={styles.ratingText}>{movieDetails.rating.toFixed(1)}</Text>
						</View>
						<View style={styles.genresContainer}>
							{movieDetails.genres && movieDetails.genres.map((genre, index) => (
								<View key={index} style={styles.genreBadge}>
									<Text style={styles.genreText}>{genre}</Text>
								</View>
							))}
						</View>
					</View>
				</View>

				<View style={styles.infoBlock}>
					<Text style={styles.subtitle}>Director: {movieDetails.director}</Text>
					<Text style={styles.subtitle}>Writers: {movieDetails.writer}</Text>
					<Text style={styles.subtitle}>Stars: {movieDetails.stars.join(', ')}</Text>
					<Text style={styles.overview}>{movieDetails.overview}</Text>
					<Text style={styles.subtitle}>Release Date: {moment(movieDetails.release_date).format('MM/DD/YYYY')}</Text>

					{/* More Like This Section */}
					<Text style={styles.moreLikeThisTitle}>More Like This:</Text>
					<ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.moreLikeThisContainer}>
						{movieDetails.more_like_this && movieDetails.more_like_this.length > 0 ? (
							movieDetails.more_like_this.map((movie, index) => (
								<TouchableOpacity
									key={index}
									style={styles.moreLikeThisItem}
									onPress={() => navigation.push('MovieDetails', { movieId: movie.movie_id })}
								>
									<Image source={{ uri: movie.image }} style={styles.moreLikeThisImage} />
									<Text style={styles.moreLikeThisText}>{movie.title}</Text>
								</TouchableOpacity>
							))
						) : (
							<Text style={styles.noRecommendations}>No recommendations available</Text>
						)}
					</ScrollView>
				</View>
			</View>
		</ScrollView>
	);
};

const styles = StyleSheet.create({
	container: {
		flex: 1,
		backgroundColor: '#fff',
	},
	loading: {
		flex: 1,
		justifyContent: 'center',
		alignItems: 'center',
	},
	errorText: {
		color: '#8b0000',
		textAlign: 'center',
		marginTop: 20,
	},
	topSection: {
		position: 'relative',
		height: 300,
		backgroundColor: '#000',
		overflow: 'hidden',
	},
	backgroundImage: {
		width: '100%',
		height: '100%',
		opacity: 0.6,
	},
	backButton: {
		position: 'absolute',
		top: 40,
		left: 20,
		zIndex: 10,
	},
	posterContainer: {
		position: 'absolute',
		top: -160,
		left: 20,
		flexDirection: 'row',
		alignItems: 'center',
		zIndex: 1,
	},
	poster: {
		width: 140,
		height: 200,
		borderRadius: 10,
		shadowColor: '#000',
		shadowOffset: { width: 0, height: 4 },
		shadowOpacity: 0.3,
		shadowRadius: 4,
	},
	movieInfo: {
		marginTop: 90,
		marginLeft: 20,
		flex: 1,
		backgroundColor: 'rgba(255, 255, 255, 0.9)',
		padding: 10,
		borderRadius: 10,
	},
	infoBlock: {
		marginTop: 50,
	},
	title: {
		fontSize: 20,
		fontWeight: 'bold',
		color: '#000',
		marginBottom: 5,
		flexWrap: 'wrap',
	},
	ratingContainer: {
		flexDirection: 'row',
		alignItems: 'center',
		marginBottom: 10,
	},
	ratingText: {
		fontSize: 16,
		color: '#8b0000',
		marginLeft: 5,
	},
	genresContainer: {
		flexDirection: 'row',
		flexWrap: 'wrap',
	},
	genreBadge: {
		backgroundColor: '#8b0000',
		borderRadius: 15,
		paddingHorizontal: 10,
		paddingVertical: 5,
		marginRight: 5,
		marginBottom: 5,
	},
	genreText: {
		fontSize: 12,
		color: '#fff',
	},
	detailsContainer: {
		marginTop: 80,
		paddingHorizontal: 20,
		borderTopRightRadius: 25,
		borderTopLeftRadius: 25,
		backgroundColor: '#fff',
	},
	subtitle: {
		fontSize: 16,
		color: '#555',
		marginBottom: 10,
	},
	overview: {
		fontSize: 16,
		color: '#333',
		marginBottom: 20,
	},
	moreLikeThisTitle: {
		fontSize: 20,
		fontWeight: 'bold',
		color: '#8b0000',
		marginBottom: 10,
	},
	moreLikeThisContainer: {
		flexDirection: 'row',
	},
	moreLikeThisItem: {
		marginRight: 15,
	},
	moreLikeThisImage: {
		width: 100,
		height: 150,
		borderRadius: 10,
	},
	moreLikeThisText: {
		width: 100,
		textAlign: 'center',
		marginTop: 5,
		fontSize: 14,
		color: '#333',
	},
	noRecommendations: {
		color: '#999',
		fontSize: 14,
		marginTop: 5,
	},
});

export default MovieDetails;
