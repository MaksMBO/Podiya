from django.contrib import admin
from .models import Event, Review, Tag, City


class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    search_fields = ('id', 'name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    search_fields = ('id', 'name',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'review_text', 'user', 'event', 'rating',)
    list_display_links = ('id', 'review_text', 'user', 'event', 'rating',)
    search_fields = ('id', 'review_text', 'user__username', 'event__name',)


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'creator', 'price',)
    list_display_links = ('id', 'name', 'city', 'creator', 'price',)
    search_fields = ('id', 'name', 'city__name', 'creator__username',)


admin.site.register(Event, EventAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(City, CityAdmin)
