from django.contrib import admin

from .models import PaymentCard, TransactionHistory

admin.site.register(PaymentCard)
admin.site.register(TransactionHistory)
