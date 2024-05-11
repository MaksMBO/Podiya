from django.core.management.base import BaseCommand
from events.management.commands import seed_events, seed_tags, seed_reviews, seed_cities
from finances.management.commands import seed_payment_cards, seed_transaction_history
from users.management.commands import seed_users, seed_user_profiles, seed_content_maker_requests, seed_issue_requests
from tickets.management.commands import seed_tickets


class Command(BaseCommand):
    help = 'Run all custom commands from all apps'

    def handle(self, *args, **options):
        self.stdout.write("Запуск всіх команд застосунку users...")
        seed_users.Command().handle()
        seed_content_maker_requests.Command().handle()
        seed_issue_requests.Command().handle()
        seed_user_profiles.Command().handle()

        self.stdout.write("Запуск всіх команд застосунку events...")
        seed_cities.Command().handle()
        seed_tags.Command().handle()
        seed_events.Command().handle()
        seed_reviews.Command().handle()

        self.stdout.write("Запуск всіх команд застосунку finances...")
        seed_payment_cards.Command().handle()
        seed_transaction_history.Command().handle()

        self.stdout.write("Запуск всіх команд застосунку tickets...")
        seed_tickets.Command().handle()
