from rest_framework import generics, status
from rest_framework.response import Response

from finances.models import PaymentCard, TransactionHistory
from finances.serializers.transaction_history import TransactionHistorySerializer


class TransactionCreateView(generics.CreateAPIView):
    """
    API view for creating a transaction.
    """
    queryset = TransactionHistory.objects.all()
    serializer_class = TransactionHistorySerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new transaction.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        card_id = serializer.validated_data.get('payment_card')
        payment_card = PaymentCard.objects.filter(id=card_id.id, user=user).first()

        if not payment_card:
            return Response({"error": "The user is not the owner of the card"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
