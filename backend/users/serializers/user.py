from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import UserProfile

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user.
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserProfileEditSerializer(serializers.ModelSerializer):
    """
    Serializer for editing user profile information.
    """

    class Meta:
        model = UserProfile
        fields = ('about',)


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile information.
    """

    class Meta:
        model = UserProfile
        fields = ('about', 'followers')


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user data.

    It serializes the user's basic information including username, email,
    avatar, staff/superuser/content maker status, profile data, and registration date.
    """
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = (
            'username', 'email', 'avatar', 'is_staff', 'is_superuser', 'is_content_maker', 'profile',
            'registration_date')


class UserEditSerializer(serializers.ModelSerializer):
    """
    Serializer for editing user information.
    """

    class Meta:
        model = User
        fields = ('username', 'avatar')


class UserAndProfileEditSerializer(serializers.Serializer):
    """
    Serializer for editing both user and profile information.

    It handles the update of both user and profile data and validates
    the input accordingly.
    """
    user = UserEditSerializer(required=False)
    profile = UserProfileEditSerializer(required=False)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        profile_data = validated_data.pop('profile', {})

        user_instance = instance.user
        profile_instance = instance

        if not user_data and not profile_data:
            message = {"error": "To edit, you need to enter user or profile data."}
            raise serializers.ValidationError(message)

        if user_data:
            for attr, value in user_data.items():
                setattr(user_instance, attr, value)
            user_instance.save()

        if profile_data:
            for attr, value in profile_data.items():
                setattr(profile_instance, attr, value)
            profile_instance.save()

        return instance


class EmailSerializer(serializers.Serializer):
    """
    Serializer for email data.
    """
    email = serializers.EmailField()


class PasswordCodeValidateSerializer(serializers.Serializer):
    """
    Serializer for validating email and code for password reset.
    """
    email = serializers.EmailField()
    code = serializers.IntegerField()


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing the user's password.
    """
    email = serializers.EmailField()
    new_password = serializers.CharField()
