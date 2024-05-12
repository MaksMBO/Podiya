from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError

from helper.image_info import handle_image


class Event(models.Model):
    """
    Model representing an event.

    Methods:
        save: Custom save method to handle validation and image processing.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    city = models.ForeignKey("events.City",
                             on_delete=models.CASCADE,
                             related_name='events')
    location_info = models.CharField(max_length=255)
    time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField("events.Tag",
                                  related_name="events",
                                  name="tags")
    creator = models.ForeignKey(get_user_model(),
                                on_delete=models.CASCADE,
                                related_name='events')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Custom save method to handle validation and image processing.

        Raises:
            ValidationError: If the creator does not have the required attributes.
        """
        if (not hasattr(self.creator, 'is_staff') and
                not hasattr(self.creator, 'is_content_maker')):
            raise ValidationError(
                "The creator must have at least one of the following attributes: 'is_staff' or 'is_content_maker'.")
        super().save(*args, **kwargs)
        handle_image(self, self.image)
