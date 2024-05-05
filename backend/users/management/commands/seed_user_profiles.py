from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import UserProfile
from random import sample, randint


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

                profile = UserProfile(
                    user=user,
                )
                profile.full_clean()
                profile.save()

                # Вибираємо фоловерів, які ще не включають оброблюваного користувача
                followers = [follower for follower in users if follower != user]
                # Обмежуємо кількість фоловерів для кожного користувача
                followers = sample(followers, k=randint(0, len(users) - 1))
                profile.followers.add(*followers)
                profile.save()
            self.stdout.write(self.style.SUCCESS("Профілі користувачів успішно створені!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Помилка: {e}. Профілі користувачів не створені"))
