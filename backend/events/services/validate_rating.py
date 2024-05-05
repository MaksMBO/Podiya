from django.core.exceptions import ValidationError


def validate_rating(value):
    if value < 0 or value > 5:
        raise ValidationError('Оцінка має бути від 0 до 5.')
