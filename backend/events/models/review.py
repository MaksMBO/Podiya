from django.contrib.auth import get_user_model
from django.db import models

from events.services.validate_rating import validate_rating


class Review(models.Model):
    review_text = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0, validators=[validate_rating])
    review_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name='reviews')
    event = models.ForeignKey("events.Event",
                              on_delete=models.CASCADE,
                              related_name='reviews')

    def __str__(self):
        return self.review_text
