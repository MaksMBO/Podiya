from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import UserProfile

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('about', 'followers')


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'email', 'avatar', 'is_staff', 'is_superuser', 'is_content_maker', 'profile', 'registration_date')


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'avatar')


class UserProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('about',)


class UserAndProfileEditSerializer(serializers.Serializer):
    user = UserEditSerializer(required=False)
    profile = UserProfileEditSerializer(required=False)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        profile_data = validated_data.pop('profile', {})

        user_instance = instance.user
        profile_instance = instance

        if not user_data and not profile_data:
            message = {"error": "Для редагування потрібно ввести дані користувача або профілю."}
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
    email = serializers.EmailField()


class PasswordCodeValidateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.IntegerField()
