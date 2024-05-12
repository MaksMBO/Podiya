from rest_framework import serializers
from finances.models import PaymentCard


class PaymentCardSerializer(serializers.ModelSerializer):
    """
    Serializer for PaymentCard model instances.
    """

    class Meta:
        model = PaymentCard
        fields = '__all__'
