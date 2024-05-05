from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from events.models import Review, Event
from random import choice, randint
from faker import Faker

fake = Faker('uk_UA')


class Command(BaseCommand):
    help = 'Seed random reviews'

    def handle(self, *args, **kwargs):
        try:
            users = get_user_model().objects.all()
            events = Event.objects.all()
            for _ in range(20):
                user = choice(users)
                event = choice(events)
                review = Review(
                    review_text=fake.text(max_nb_chars=200),
                    rating=randint(0, 10) / 2.0,
                    user=user,
                    event=event,
                )
                review.full_clean()
                review.save()
            self.stdout.write(self.style.SUCCESS("Відгуки успішно створені!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Помилка: {e}. Відгуки не створені"))
