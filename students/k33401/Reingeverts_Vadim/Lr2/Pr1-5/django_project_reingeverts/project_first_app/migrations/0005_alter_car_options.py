# Generated by Django 4.1.5 on 2023-01-14 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_first_app', '0004_delete_carownsershipmodel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='car',
            options={'verbose_name': models.F('model')},
        ),
    ]