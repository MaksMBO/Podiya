from django.contrib.auth import get_user_model
from django.db import models


class Review(models.Model):
    review_text = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name='reviews')
    event = models.ForeignKey("events.Event",
                              on_delete=models.CASCADE,
                              related_name='reviews')

    def __str__(self):
        return self.review_text
