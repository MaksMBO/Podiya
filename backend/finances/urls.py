from django.urls import path
from .views.transaction_history import TransactionCreateView
from .views.payment_card import PaymentCardListCreateAPIView, PaymentCardRetrieveDestroyAPIView

urlpatterns = [
    path('cards/', PaymentCardListCreateAPIView.as_view(), name='payment-card-list-create'),
    path('cards/<int:id>/', PaymentCardRetrieveDestroyAPIView.as_view(), name='payment-card-retrieve-destroy'),
    path('create-transaction/', TransactionCreateView.as_view(), name='create-transaction'),
]
