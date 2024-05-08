from rest_framework import generics, pagination
from rest_framework.permissions import IsAuthenticated
from .models import Ticket
from .serializers import TicketSerializer


class UserTicketView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user).select_related('user')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SingleUserTicketView(generics.RetrieveAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user).select_related('user')
