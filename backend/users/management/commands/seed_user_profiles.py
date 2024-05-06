from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker

from users.models import UserProfile
from random import sample, randint

fake = Faker('uk_UA')


class Command(BaseCommand):
    help = 'Seed random user profiles'

    def handle(self, *args, **kwargs):
        try:
            users = list(get_user_model().objects.all())
            for user in users:
                try:
                    UserProfile.objects.get(user=user)
                    self.stdout.write(self.style.WARNING(f"Профіль користувача {user} вже існує. Пропускаю."))
                    continue
                except UserProfile.DoesNotExist:
                    pass

                if user.is_staff or user.is_content_maker:
                    profile = UserProfile(
                        user=user,
                        about=fake.text(max_nb_chars=300),
                    )
                else:
                    profile = UserProfile(user=user)
                profile.full_clean()
                profile.save()

                followers = [follower for follower in users if follower != user]
                followers = sample(followers, k=randint(0, len(users) - 1))
                profile.followers.add(*followers)
                profile.save()
            self.stdout.write(self.style.SUCCESS("Профілі користувачів успішно створені!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Помилка: {e}. Профілі користувачів не створені"))
