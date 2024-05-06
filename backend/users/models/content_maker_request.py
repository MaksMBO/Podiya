from django.db import models
from django.contrib.auth import get_user_model


class ContentMakerRequest(models.Model):
    text = models.TextField()
    is_approved = models.BooleanField(default=False)
    request_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='content_maker_requests')

    def __str__(self):
        return f"Запит {self.user} на отримання ролі контентмейкера"
