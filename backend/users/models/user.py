from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from helper.image_info import handle_image


class CustomUserManager(BaseUserManager):
    """
    Custom manager for the User model.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user.
        """
        if not email:
            raise ValueError('The e-mail field must be filled')
        if not extra_fields.get('username'):
            raise ValueError('Username field must be filled')
        if not password:
            raise ValueError('The password must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_content_maker', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_content_maker') is not True:
            raise ValueError('Superuser must have is_content_maker=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.
    """
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

    def change_password(self, new_password):
        """
        Change the user's password.
        """
        self.password = make_password(new_password)
        self.save()

    def save(self, *args, **kwargs):
        """
        Save the user object.

        This method overrides the save method to handle avatar image upload.
        """
        super().save(*args, **kwargs)
        handle_image(self, self.avatar)
