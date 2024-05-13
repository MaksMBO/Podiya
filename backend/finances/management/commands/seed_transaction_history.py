from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from finances.models import PaymentCard, TransactionHistory
from events.models import Event
from random import choice, randint
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Seed random transaction histories'

    def handle(self, *args, **kwargs):
        try:
            users = get_user_model().objects.all()
            events = Event.objects.all()
            payment_cards = PaymentCard.objects.all()
            for _ in range(250):
                user = choice(users)
                cards = choice(payment_cards)
                card = cards
                event = choice(events)
                transaction_date = datetime.now() - timedelta(days=randint(1, 365))
                transaction = TransactionHistory(transaction_date=transaction_date,
                                                 user=user, payment_card=card,
                                                 event=event)
                transaction.full_clean()
                transaction.save()
            self.stdout.write(self.style.SUCCESS("Історії транзакцій успішно створені!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Помилка: {e}. Історія транзакцій не створена"))
