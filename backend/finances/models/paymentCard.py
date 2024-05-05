from django.contrib.auth import get_user_model
from django.db import models

from finances.services.validate_card_number import validate_card_number


class PaymentCard(models.Model):
    last_four_digits = models.CharField(max_length=16, validators=[validate_card_number])
    registration_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name='user_payment_cards')

    def __str__(self):
        return f'Карта {self.user}'

    def save(self, *args, **kwargs):
        self.last_four_digits = self.last_four_digits[-4:]
        super(PaymentCard, self).save(*args, **kwargs)
