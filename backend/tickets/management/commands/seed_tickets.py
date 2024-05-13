from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from tickets.models import Ticket
from events.models import Event
from random import choice
from faker import Faker

fake = Faker('uk_UA')  # Ukrainian locale


class Command(BaseCommand):
    help = 'Seed random tickets'

    def handle(self, *args, **kwargs):
        try:
            users = get_user_model().objects.all()
            events = Event.objects.all()
            for _ in range(100):
                user = choice(users)
                event = choice(events)
                ticket = Ticket(
                    user=user,
                    event=event,
                )
                ticket.full_clean()
                ticket.save()
            self.stdout.write(self.style.SUCCESS("Квитки успішно створені!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Помилка: {e}. Квитки не створені"))
