from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import PaymentCard, TransactionHistory
from .serializers import PaymentCardSerializer, TransactionHistorySerializer


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


class TransactionCreateView(generics.CreateAPIView):
    queryset = TransactionHistory.objects.all()
    serializer_class = TransactionHistorySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        card_id = serializer.validated_data.get('payment_card')
        payment_card = PaymentCard.objects.filter(id=card_id.id, user=user).first()

        if not payment_card:
            return Response({"error": "Користувач не є власником карти"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
