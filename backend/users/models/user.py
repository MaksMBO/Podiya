from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from helper.image_info import handle_image


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле електронної пошти повинне бути заповненим')
        if not extra_fields.get('username'):
            raise ValueError('Поле імені користувача повинне бути заповненим')
        if not password:
            raise ValueError('Пароль повинен бути встановленим')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_content_maker', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/no_avatar.webp')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_content_maker = models.BooleanField(default=False)

    registration_date = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        handle_image(self, self.avatar)
