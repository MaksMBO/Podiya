# Generated by Django 5.0.4 on 2024-05-06 18:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0002_initial'),
        ('finances', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentcard',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_payment_cards', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transactionhistory',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_transaction_history', to='events.event'),
        ),
        migrations.AddField(
            model_name='transactionhistory',
            name='payment_card',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_card_transaction_history', to='finances.paymentcard'),
        ),
        migrations.AddField(
            model_name='transactionhistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_transaction_history', to=settings.AUTH_USER_MODEL),
        ),
    ]
