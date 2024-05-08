from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import PaymentCard
from .serializers import PaymentCardSerializer


class PaymentCardListCreateAPIView(generics.ListCreateAPIView):
    """
    API view for listing and creating payment cards.
    """
    serializer_class = PaymentCardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Method to filter queryset based on the authenticated user.
        """
        return PaymentCard.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Method to set the user field on card creation.
        """
        serializer.save(user=self.request.user)


class PaymentCardRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    """
    API view for retrieving and deleting a payment card.
    """
    queryset = PaymentCard.objects.all()
    serializer_class = PaymentCardSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Method to filter queryset based on the authenticated user.
        """
        return self.queryset.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        Method to handle delete operation with permission check.
        """
        instance = self.get_object()
        if instance.user != request.user:
            raise PermissionDenied("You don't have permission to delete this card.")
        return super().destroy(request, *args, **kwargs)
