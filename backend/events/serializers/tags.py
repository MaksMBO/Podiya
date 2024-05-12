from rest_framework import serializers

from events.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model instances.
    """

    class Meta:
        model = Tag
        fields = '__all__'


class RatingTagSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying tag name and its average rating.
    """
    average_rating = serializers.FloatField()

    class Meta:
        model = Tag
        fields = ['name', 'average_rating']
