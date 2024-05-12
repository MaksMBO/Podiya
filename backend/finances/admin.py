from django.contrib import admin

from .models import PaymentCard, TransactionHistory


class TransactionHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'payment_card', 'event', 'transaction_date',)
    list_display_links = ('id', 'user', 'payment_card', 'event', 'transaction_date',)
    search_fields = ('id', 'user', 'event',)


class PaymentCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'registration_date',)
    list_display_links = ('id', 'user', 'registration_date',)
    search_fields = ('id', 'user',)


admin.site.register(PaymentCard, PaymentCardAdmin)
admin.site.register(TransactionHistory, TransactionHistoryAdmin)
