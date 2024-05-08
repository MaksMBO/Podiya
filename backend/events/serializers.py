from django.db.models import Avg
from rest_framework import serializers
from .models import Tag, Event, Review


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_rating(self, obj):
        average_rating = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        if average_rating is None:
            return 0
        return round(average_rating, 1)


class EventUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ('price', 'location')


class ReviewSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('review_text', 'rating', 'user', 'review_date')


class ReviewSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('review_text', 'rating', 'user')