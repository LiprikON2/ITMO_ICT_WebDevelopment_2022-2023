# Generated by Django 4.1.5 on 2023-01-22 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_remove_flight_reservations'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flight',
            old_name='fligt_number',
            new_name='flight_number',
        ),
    ]