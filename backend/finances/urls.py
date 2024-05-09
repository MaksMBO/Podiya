from django.urls import path
from .views import PaymentCardListCreateAPIView, PaymentCardRetrieveDestroyAPIView, TransactionCreateView

urlpatterns = [
    path('cards/', PaymentCardListCreateAPIView.as_view(), name='payment-card-list-create'),
    path('cards/<int:id>/', PaymentCardRetrieveDestroyAPIView.as_view(), name='payment-card-retrieve-destroy'),
    path('create-transaction/', TransactionCreateView.as_view(), name='create-transaction'),
]
