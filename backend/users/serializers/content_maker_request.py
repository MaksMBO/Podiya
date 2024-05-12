from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import ContentMakerRequest

User = get_user_model()


class ContentMakerRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for handling content maker requests.
    """

    class Meta:
        model = ContentMakerRequest
        fields = '__all__'
        read_only_fields = ('request_date', 'user')


class ContentMakerRequestUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating content maker requests.
    """

    class Meta:
        model = ContentMakerRequest
        fields = ['is_approved']
