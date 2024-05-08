import random
import redis

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.generics import (
    CreateAPIView, RetrieveAPIView, UpdateAPIView,
)

from django.contrib.auth import get_user_model

from helper.errors import get_errors_as_string
from .models import UserProfile
from .serializers import UserCreateSerializer, UserSerializer, UserAndProfileEditSerializer, EmailSerializer, \
    PasswordCodeValidateSerializer
from .services import handle_user

redis_con = redis.Redis(decode_responses=True)


class UserCreateAPIView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # TODO
        # email = request.data.get('email')
        # if not email:
        #     return Response(
        #         {"message": "Email відсутній"},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        #
        # if not redis_con.get(email + "_verified"):
        #     return Response(
        #         {"message": "Email не підтверджено"},
        #         status=status.HTTP_403_FORBIDDEN
        #     )

        response = super().create(request, *args, **kwargs)
        # redis_con.delete(email + "_verified")

        return response


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserAndProfileEditAPIView(UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserAndProfileEditSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class UserLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        required_fields = ['username', 'email', 'password']
        missing_fields = [field for field in required_fields if not request.data.get(field)]

        if missing_fields:
            return Response({'error': f"Будь ласка, вкажіть {', '.join(missing_fields)}"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(**request.data)

        if user is None:
            return Response({'error': 'Недійсні облікові дані'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class AccessRecoveryApiView(APIView):
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
            return Response({'detail': 'Токен застарів або не дійсний'},
                            status=status.HTTP_400_BAD_REQUEST)


class EmailSendCodeView(APIView):

    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            code = random.randint(100000, 999999)
            # TODO
            # redis_con.set(serializer.data['email'], code, "300")
            handle_user.handle_send_email_verify(
                serializer.data['email'],
                code
            )
            return Response("Okay", status=status.HTTP_200_OK)

        message = get_errors_as_string(serializer)
        return Response({"message": message}, status=status.HTTP_403_FORBIDDEN)


class CodeValidateApiView(APIView):

    def post(self, request):
        serializer = PasswordCodeValidateSerializer(data=request.data)
        if serializer.is_valid():
            # real_code = redis_con.get(serializer.data['email'])
            # if not real_code:
            #     return Response(
            #         {"message": "Verification code is expired"},
            #         status=status.HTTP_403_FORBIDDEN
            #     )
            #
            # is_valid = int(real_code) == serializer.data['code']
            # if is_valid:
            #     redis_con.delete(serializer.data['email'])
            #     redis_con.set(serializer.data['email'] + "_verified", int(True))
            if serializer.data['code'] == 111111:
                is_valid = False
            else:
                is_valid = True

            return Response({"valid": is_valid}, status=status.HTTP_200_OK)

        return Response("Okay", status=status.HTTP_200_OK)
