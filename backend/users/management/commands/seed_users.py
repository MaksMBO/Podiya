from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random

fake = Faker('uk_UA')

class Command(BaseCommand):
    help = 'Seed random users'

    def handle(self, *args, **kwargs):
        try:
            for _ in range(20):
                User = get_user_model()
                user = User(
                    username=fake.user_name(),
                    email=fake.email(),
                    is_active=True,
                    is_staff=random.choice([True, False]),
                    is_content_maker=random.choice([True, False]),
                )
                user.set_password('Test1234')
                user.full_clean()
                user.save()
            self.stdout.write(self.style.SUCCESS("Користувачі успішно створені!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Помилка: {e}. Користувачі не створені"))
