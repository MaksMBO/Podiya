from rest_framework import generics, pagination
from rest_framework.permissions import IsAuthenticated
from tickets.models import Ticket
from tickets.serializers.tickets import TicketSerializer


class UserTicketView(generics.ListCreateAPIView):
    """
    API view for listing and creating tickets for the authenticated user.

    Methods:
        get_queryset: Returns the queryset for listing tickets.
        perform_create: Custom method to set the user when creating a ticket.
    """
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        """
        Returns the queryset for listing tickets.
        """
        return Ticket.objects.filter(user=self.request.user).select_related('user')

    def perform_create(self, serializer):
        """
        Custom method to set the user when creating a ticket.
        """
        serializer.save(user=self.request.user)


class SingleUserTicketView(generics.RetrieveAPIView):
    """
    API view for retrieving a single ticket for the authenticated user.
    """
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns the queryset for retrieving the ticket.
        """
        return Ticket.objects.filter(user=self.request.user).select_related('user')
