from django.db import models


class City(models.Model):
    """
    Model representing a city.
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
