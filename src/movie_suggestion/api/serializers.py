from rest_framework import serializers
from .models import MovieRecommendation


class MovieRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieRecommendation
        fields = ['id', 'user', 'movieId', 'title', 'voteAverage', 'expireAt', 'imageUrl', 'type']
