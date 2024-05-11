from django.core.management.base import BaseCommand

from events.models import City
from helper.parser_of_cities import get_cities


class Command(BaseCommand):
    help = 'Seed random cities'

    def handle(self, *args, **kwargs):
        all_sities = get_cities()
        for city in all_sities:
            try:
                tag = City(
                    name=city,
                )
                tag.full_clean()
                tag.save()
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Місно {city} не створено. Помилка: {e}"))

        self.stdout.write(self.style.SUCCESS("Міста успішно створені!"))
