from rest_framework import serializers
from .models import PaymentCard


class PaymentCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentCard
        fields = '__all__'
