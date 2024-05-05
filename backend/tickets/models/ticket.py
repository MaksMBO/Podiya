from django.db import models
from django.contrib.auth import get_user_model
import uuid

from tickets.services.generate_qr_code import generate_qr_code


class Ticket(models.Model):
    purchase_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='tickets')
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, related_name='tickets')
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return f'Білет на поідію {self.event.name}, для {self.user}'

    def save(self, *args, **kwargs):
        ticket_info = self.__str__()
        self.qr_code.save(f'ticket_{uuid.uuid4()}.png', generate_qr_code(ticket_info), save=False)
        super().save(*args, **kwargs)
