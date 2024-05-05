from django.core.management.base import BaseCommand
from events.models import Tag
from faker import Faker

fake = Faker('uk_UA')


class Command(BaseCommand):
    help = 'Seed random tags'

    def handle(self, *args, **kwargs):
        try:
            for _ in range(20):
                tag = Tag(
                    name=fake.word(),
                )
                tag.full_clean()
                tag.save()
            self.stdout.write(self.style.SUCCESS("Теги успішно створені!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Помилка: {e}. Теги не створені"))
