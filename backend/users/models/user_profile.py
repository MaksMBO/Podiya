from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model


class UserProfile(models.Model):
    """
    Model representing user profiles.
    """
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
        """
        Override the save method to ensure associated user has necessary attributes.
        """
        if (not hasattr(self.user, 'is_staff') and
                not hasattr(self.user, 'is_content_maker')):
            raise ValidationError(
                "The creator must have at least one of the following attributes: 'is_staff' or 'is_content_maker'.")
        super().save(*args, **kwargs)
