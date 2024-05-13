from django.core.management.base import BaseCommand
from events.models import Tag
from faker import Faker

fake = Faker('uk_UA')

tags = ['Концерти', 'Змагання', 'Фестивалі', 'Літературний вечір', 'Благодійність', 'Виставки', 'Менторські зустрічі',
        'Стендап', 'Вуличний театр', 'Майстер-класи', 'Кінофестивалі', 'Ярмарки', 'Спортивні заходи', 'Зустрічі з йоги',
        'Туристичні екскурсії', 'Воркшопи', 'Танцювальні класи', 'Книжкові клуби', 'Медитаційні сесії',
        'Відкриті мікрофони', 'Віртуальна реальність', 'Кулінарні майстер-класи']


class Command(BaseCommand):
    help = 'Seed random tags'

    def handle(self, *args, **kwargs):
        try:
            for one_tag in tags:
                tag = Tag(
                    name=one_tag,
                )
                tag.full_clean()
                tag.save()
            self.stdout.write(self.style.SUCCESS("Теги успішно створені!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Помилка: {e}. Теги не створені"))
