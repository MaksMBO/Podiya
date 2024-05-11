from django.contrib import admin
from .models import Event, Review, Tag, City

admin.site.register(Event)
admin.site.register(Review)
admin.site.register(Tag)
admin.site.register(City)
