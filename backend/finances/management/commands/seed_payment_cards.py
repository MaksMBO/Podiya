from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from finances.models import PaymentCard

categories = ["4999999999990011", "4999999999990029", "5559490000000148", "5559490000000106"]


class Command(BaseCommand):
    help = 'Seed random payment cards'

    def handle(self, *args, **kwargs):
        try:
            user = get_user_model().objects.first()
            for category_name in categories:
                card = PaymentCard(user=user, last_four_digits=category_name)
                card.full_clean()
                card.save()
            self.stdout.write(self.style.SUCCESS("Банківські карти успішно створені!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Помилка: {e}. Банківська карта не створена"))
