from rest_framework import serializers
from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    movie_type = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        required=False,
        slug_field='title')

    class Meta:
        model = Movie
        fields = ('id', 'title', 'original_title', 'movie_type')
