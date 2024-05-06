from django.db import models
from django.contrib.auth import get_user_model


class IssueRequest(models.Model):
    text = models.TextField()
    request_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='issue_request')

    def __str__(self):
        return f"Інформація від {self.user}"
