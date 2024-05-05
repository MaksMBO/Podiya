from django.db import models
from django.contrib.auth import get_user_model


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(),
                                on_delete=models.CASCADE,
                                related_name='profile')
    followers = models.ManyToManyField(get_user_model(),
                                       related_name='following',
                                       blank=True,
                                       name='followers')

    def __str__(self):
        return self.user
