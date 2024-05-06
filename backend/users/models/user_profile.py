from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model


class UserProfile(models.Model):
    about = models.TextField(blank=True, null=True)
    user = models.OneToOneField(get_user_model(),
                                on_delete=models.CASCADE,
                                related_name='profile')
    followers = models.ManyToManyField(get_user_model(),
                                       related_name='following',
                                       blank=True,
                                       name='followers')

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        if (not hasattr(self.user, 'is_staff') and
                not hasattr(self.user, 'is_content_maker')):
            raise ValidationError(
                "Створювач повинен мати принаймні один з наступних атрибутів: 'is_staff' або 'is_content_maker'.")
        super().save(*args, **kwargs)
