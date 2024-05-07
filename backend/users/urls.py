from django.urls import path

from .views import UserLoginAPIView, AccessRecoveryApiView, UserCreateAPIView, UserRetrieveAPIView, \
    UserAndProfileEditAPIView, EmailSendCodeView, CodeValidateApiView

urlpatterns = [
    path(r'user-profile/edit/', UserAndProfileEditAPIView.as_view(), name='user-profile-edit'),
    path(r'about-me/', UserRetrieveAPIView.as_view(), name='user-detail'),
    path(r'create/', UserCreateAPIView.as_view(), name='user-create'),
    path(r'login/', UserLoginAPIView.as_view(), name='api-token-auth'),
    path(r'token-refresh/', AccessRecoveryApiView.as_view(), name='api-token-refresh'),
    path(r'email_verify/', EmailSendCodeView.as_view(), name='email_verify'),
    path(r'email_verify_validate/', CodeValidateApiView.as_view(), name='email_verify_validate'),
]
