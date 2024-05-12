from rest_framework import serializers
from tickets.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    """
    Serializer for Ticket model instances.
    """

    class Meta:
        model = Ticket
        fields = '__all__'
