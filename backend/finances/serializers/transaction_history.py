from rest_framework import serializers
from finances.models import TransactionHistory


class TransactionHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for TransactionHistory model instances.
    """

    class Meta:
        model = TransactionHistory
        fields = '__all__'
