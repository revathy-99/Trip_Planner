# Generated by Django 5.1.2 on 2025-01-06 07:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Trip_app', '0024_booking_payment_status_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='package',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Trip_app.trippackage'),
        ),
    ]