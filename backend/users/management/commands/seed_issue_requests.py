from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker

from users.models import IssueRequest
from random import choice

fake = Faker('uk_UA')


class Command(BaseCommand):
    help = 'Seed random issue requests'

    def handle(self, *args, **kwargs):
        try:
            users = get_user_model().objects.all()
            for _ in range(20):
                user = choice(users)
                request = IssueRequest(
                    user=user,
                    text=fake.text(max_nb_chars=100)
                )
                request.full_clean()
                request.save()
            self.stdout.write(self.style.SUCCESS("Запити повідомлення про помилку успішно створені!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Помилка: {e}. Запити на повідомлення про помилку не створені"))
