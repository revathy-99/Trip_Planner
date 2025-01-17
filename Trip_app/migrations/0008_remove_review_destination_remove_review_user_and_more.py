# Generated by Django 5.1.2 on 2024-12-30 09:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Trip_app', '0007_destination_tripcategory_remove_usertrip_trip_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='destination',
        ),
        migrations.RemoveField(
            model_name='review',
            name='user',
        ),
        migrations.AlterField(
            model_name='destination',
            name='category',
            field=models.CharField(choices=[('Adventure', 'Adventure'), ('Leisure', 'Leisure')], default='Leisure', max_length=20),
        ),
        migrations.RenameField(
            model_name='destination',
            old_name='location',
            new_name='country',
        ),
        migrations.RemoveField(
            model_name='destination',
            name='available_dates',
        ),
        migrations.RemoveField(
            model_name='destination',
            name='price',
        ),
        migrations.AddField(
            model_name='destination',
            name='price_range',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='destination',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='destinations/'),
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('available_dates', models.JSONField()),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Trip_app.destination')),
            ],
        ),
        migrations.CreateModel(
            name='UserTripCustomization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selected_dates', models.JSONField()),
                ('activities', models.JSONField(blank=True, null=True)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Trip_app.trip')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Itinerary',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
        migrations.DeleteModel(
            name='TripCategory',
        ),
    ]
