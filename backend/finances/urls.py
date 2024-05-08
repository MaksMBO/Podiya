from django.urls import path
from .views import PaymentCardListCreateAPIView, PaymentCardRetrieveDestroyAPIView

urlpatterns = [
    path('cards/', PaymentCardListCreateAPIView.as_view(), name='payment-card-list-create'),
    path('cards/<int:id>/', PaymentCardRetrieveDestroyAPIView.as_view(), name='payment-card-retrieve-destroy'),
]
