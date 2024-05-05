from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError

from events.services.image_info import handle_image


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField("events.Tag",
                                  blank=True,
                                  related_name="events",
                                  name="tags")
    creator = models.ForeignKey(get_user_model(),
                                on_delete=models.CASCADE,
                                related_name='events')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if (not hasattr(self.creator, 'is_staff') and
                not hasattr(self.creator, 'is_admin') and
                not hasattr(self.creator, 'is_content_maker')):
            raise ValidationError(
                "Створювач повинен мати принаймні один з наступних атрибутів: 'is_staff', 'is_admin' або 'is_content_maker'.")
        super().save(*args, **kwargs)
        handle_image(self)
