from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserLoginAPIView, AccessRecoveryApiView, UserCreateAPIView, UserRetrieveAPIView, \
    UserAndProfileEditAPIView, EmailSendCodeView, CodeValidateApiView, PasswordResetApiView, IssueRequestViewSet, \
    ContentMakerRequestViewSet, ChangePasswordView

router = DefaultRouter()
router.register(r'issue-requests', IssueRequestViewSet, basename='issue-request')
router.register(r'content-maker-requests', ContentMakerRequestViewSet, basename='content-maker-request')

urlpatterns = [
    path(r'user-profile/edit/', UserAndProfileEditAPIView.as_view(), name='user-profile-edit'),
    path(r'about-me/', UserRetrieveAPIView.as_view(), name='user-detail'),
    path(r'create/', UserCreateAPIView.as_view(), name='user-create'),
    path(r'login/', UserLoginAPIView.as_view(), name='api-token-auth'),
    path(r'token-refresh/', AccessRecoveryApiView.as_view(), name='api-token-refresh'),
    path(r'email_verify/', EmailSendCodeView.as_view(), name='email_verify'),
    path(r'email_verify_validate/', CodeValidateApiView.as_view(), name='email_verify_validate'),
    path(r'password_reset/', PasswordResetApiView.as_view(), name="password_reset"),
    path(r'password_change_verify_validate/', CodeValidateApiView.as_view(), name='password_change_verify_validate'),
    path(r'change-password/', ChangePasswordView.as_view(), name='change_password'),
    path(r'', include(router.urls)),
]
