from rest_framework import serializers

from events.models import Review


class ReviewSerializerGet(serializers.ModelSerializer):
    """
    Serializer for retrieving Review instances.
    """

    class Meta:
        model = Review
        fields = ('review_text', 'rating', 'user', 'review_date')


class ReviewSerializerPost(serializers.ModelSerializer):
    """
    Serializer for creating Review instances.
    """

    class Meta:
        model = Review
        fields = ('review_text', 'rating', 'user')
