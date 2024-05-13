from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView, RetrieveAPIView, UpdateAPIView,
)

import random
import redis

from events.models import Event
from events.serializers.events import EventSerializer
from helper.paginator import EventPagination
from podiya.settings import config
from users.models import UserProfile
from users.serializers.user import UserCreateSerializer, UserSerializer, UserAndProfileEditSerializer, \
    EmailSerializer, PasswordCodeValidateSerializer, ChangePasswordSerializer, UserSerializerContentMaker
from users.services import handle_user
from helper.errors import get_errors_as_string

if config.get('DB_ON_SERVER') == 'True':
    redis_con = redis.Redis(host='podiya_redis', decode_responses=True)
else:
    redis_con = redis.Redis(decode_responses=True)


class UserCreateAPIView(CreateAPIView):
    """
    An endpoint for creating a new user.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # TODO
        email = request.data.get('email')
        if not email:
            return Response(
                {"error": "There is no email"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not redis_con.get(email + "_verified"):
            return Response(
                {"error": "Email not confirmed"},
                status=status.HTTP_403_FORBIDDEN
            )

        response = super().create(request, *args, **kwargs)
        redis_con.delete(email + "_verified")

        return response


class UserLoginAPIView(APIView):
    """
    Handles user login by checking credentials and generating JWT tokens.
    """

    def post(self, request, *args, **kwargs):
        required_fields = ['email', 'password']
        missing_fields = [field for field in required_fields if not request.data.get(field)]

        if missing_fields:
            return Response({'error': f"Please specify {', '.join(missing_fields)}"},
                            status=status.HTTP_400_BAD_REQUEST)

        # username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            return Response({'error': "User with such data does not exist"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(request, username=user.username, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class EmailSendCodeView(APIView):
    """
    Sends a verification code to the specified email address.
    """

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            code = random.randint(100000, 999999)
            # TODO
            redis_con.set(serializer.data['email'], code, "300")
            handle_user.handle_send_email_verify(
                serializer.data['email'],
                code
            )
            return Response("Okay", status=status.HTTP_200_OK)

        message = get_errors_as_string(serializer)
        return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)


class UserRetrieveAPIView(RetrieveAPIView):
    """
    Retrieves details of the authenticated user.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserAndProfileEditAPIView(UpdateAPIView):
    """
    Updates the authenticated user's profile.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserAndProfileEditSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class AccessRecoveryApiView(APIView):
    """
    Recovers the authenticated user's profile.
    """

    def post(self, request, *args, **kwargs):
        refresh_token_value = request.data.get('refresh')

        if refresh_token_value:
            refresh = RefreshToken(refresh_token_value)
            access_token = str(refresh.access_token)

            return Response({
                'access': access_token,
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'The token is out of date or invalid'},
                            status=status.HTTP_400_BAD_REQUEST)


class PasswordResetApiView(APIView):
    """
    Resets the authenticated user's password.
    """

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = get_user_model().objects.get(email=serializer.data['email'])
            except Exception:
                return Response(
                    {"error": "The user with this email does not exist"},
                    status=status.HTTP_403_FORBIDDEN
                )

            code = random.randint(100000, 999999)
            redis_con.set(serializer.data['email'], code, "300")
            handle_user.handle_send_email_verify(
                serializer.data['email'],
                code
            )

            return Response("Okay", status=status.HTTP_200_OK)

        message = get_errors_as_string(serializer)
        return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)


class CodeValidateApiView(APIView):
    """
    Validates the verification code sent during password reset.
    """

    def post(self, request):
        serializer = PasswordCodeValidateSerializer(data=request.data)
        if serializer.is_valid():
            real_code = redis_con.get(serializer.data['email'])
            if not real_code:
                return Response(
                    {"message": "Verification code is expired"},
                    status=status.HTTP_403_FORBIDDEN
                )

            is_valid = int(real_code) == serializer.data['code']
            if is_valid:
                redis_con.delete(serializer.data['email'])
                redis_con.set(serializer.data['email'] + "_verified", int(True))

            return Response({"valid": is_valid}, status=status.HTTP_200_OK)

        return Response("Okay", status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    """
     Allows users to change their password.
    """

    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(get_user_model(), email=serializer.validated_data['email'])
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeContentMakerStatus(APIView):
    """
    Class for changing the status of a content maker.
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, user_id):
        try:
            user = get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializerContentMaker(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSubscribedEvents(generics.ListAPIView):
    """
    API endpoint to retrieve events based on user subscriptions.
    """
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = EventPagination

    def get_queryset(self):
        try:
            user = self.request.user
            followers = user.profile.followers.all()
            subscribed_events = Event.objects.filter(creator__in=followers).select_related('creator')
            return subscribed_events
        except Exception as e:
            return Event.objects.none()
