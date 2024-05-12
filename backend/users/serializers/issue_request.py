from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import IssueRequest

User = get_user_model()


class IssueRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for handling issue request data.
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True, required=False)

    class Meta:
        model = IssueRequest
        fields = '__all__'

    def validate_user(self, value):
        """
        Validate the user field.
        """
        raise serializers.ValidationError("Unable to set value for field 'user'.")

    def validate_request_date(self, value):
        """
        Validate the request_date field.
        """
        raise serializers.ValidationError("Unable to set value for field 'request_date'.")
