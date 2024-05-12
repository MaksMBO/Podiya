from django.db.models import Avg
from rest_framework import serializers

from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for Event model.
    """
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    depth = 1

    def get_rating(self, obj):
        """
        Get the average rating of an event.
        """
        average_rating = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(average_rating or 0, 1)


class EventUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating Event model instances.
    """

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('price', 'location_info', 'city', 'creator')
