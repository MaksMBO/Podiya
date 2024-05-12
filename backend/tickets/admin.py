from django.contrib import admin
from .models import Ticket


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'event',)
    list_display_links = ('id', 'user', 'event',)
    search_fields = ('id', 'user', 'event',)


admin.site.register(Ticket, TicketAdmin)
