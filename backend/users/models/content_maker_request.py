from django.db import models
from django.contrib.auth import get_user_model


class ContentMakerRequest(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Запит {self.user} на отримання ролі контентмейкера"
