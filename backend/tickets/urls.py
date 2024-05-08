from django.urls import path
from .views import UserTicketView, SingleUserTicketView

urlpatterns = [
    path('', UserTicketView.as_view(), name='user-tickets'),
    path('<int:pk>/', SingleUserTicketView.as_view(), name='single-user-ticket'),
]
