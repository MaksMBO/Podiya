from django.contrib.auth import get_user_model
from django.db import models


class TransactionHistory(models.Model):
    transaction_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name='user_transaction_history')
    payment_card = models.ForeignKey("finances.PaymentCard",
                                     on_delete=models.CASCADE,
                                     related_name='payment_card_transaction_history')
    event = models.ForeignKey("events.Event",
                              on_delete=models.CASCADE,
                              null=True,
                              related_name='event_transaction_history')

    def __str__(self):
        return f'Транзакція користувача: {self.user}. Дата: {self.transaction_date}'
