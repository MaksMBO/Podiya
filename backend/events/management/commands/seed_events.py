from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone

from events.models import Event, Tag
from random import choice, randint
from faker import Faker

fake = Faker('uk_UA')


class Command(BaseCommand):
    help = 'Seed random events'

    def handle(self, *args, **kwargs):
        try:
            users = get_user_model().objects.filter(
                Q(is_staff=True) | Q(is_superuser=True) | Q(is_content_maker=True)
            )
            tags = list(Tag.objects.all())
            if not tags:
                self.stdout.write(self.style.ERROR(
                    "Немає жодного тегу для використання. Будь ласка, створіть деякі теги перед виконанням цієї команди."))
                return
            for _ in range(20):
                user = choice(users)
                event = Event(
                    name=fake.sentence(nb_words=5),
                    description=fake.text(max_nb_chars=200),
                    price=randint(0, 1000),
                    time=timezone.make_aware(fake.future_datetime(end_date='+30d')),
                    creator=user,
                    image=f'events/test_event.webp',
                    location=f'{fake.city()}, {fake.street_name()}, {fake.building_number()}'
                )
                event.full_clean()
                event.save()
                event.tags.add(*fake.random_elements(elements=tags, length=randint(1, min(5, len(tags))), unique=True))
                event.save()
            self.stdout.write(self.style.SUCCESS("Події успішно створені!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Помилка: {e}. Події не створені"))
